#define MAX_BITFLOW_SIZE 10000  /* The maximum number of characters to be */
                                /* parsed in a bitflow program */

/* standard C includes */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

const char EOL = '\n'; /* End of Line marker */

/* All the known characters used in bitflow */

/* Misc and i/o */
const char COMMENT_MARKER = '#';    /* comment */
const char INDEX_SPEC = '@';        /* index entry*/
const char COLON = ':';             /* delimiter*/
const char NEW_LINE_OUT = ';';      /* line break */
const char SPACE_OUT = '_';         /* space */
const char INT_OUT = '.';           /* print as int */
const char ASCII_OUT = ',';         /* print as char */

/* bit manipulation */
const char INCREMENT = '+';     /* increment */
const char DECREMENT = '-';     /* decrement */
const char MULTIPLY = '*';      /* multiply */
const char DIVIDE = '/';        /* divide */
const char POWER = '^';         /* power */

/* Value setters */
const char SET_0 = '!';     /* Set to 0 */
const char SET_64 = '&';    /* Set to 64 */
const char SET_96 = '$';    /* Set to 96 */
const char SET_A = 'a';     /* Set to 'a' */
const char SET_B = 'b';     /* Set to 'b' */

/* Loop delimiters */
const char L_BRACK = '[';
const char L_CURL = '{';
const char R_BRACK = ']';
const char R_CURL = '}';

int var_a = 0;      /* the param values */
int var_b = 0;

/* Returns an integer representation of the char param passed */
int to_int(const char* snum )
{
    int idx, strIdx = 0, accum = 0, numIsNeg = 0;
    const unsigned int NUMLEN = (int)strlen(snum);

    /* Check if negative number and flag it. */
    if(snum[0] == 0x2d)
    {
        numIsNeg = 1;
    }

    for(idx = NUMLEN - 1; idx >= 0; idx--)
    {
        /* Only process numbers from 0 through 9. */
        if(snum[strIdx] >= 0x30 && snum[strIdx] <= 0x39)
        {
            accum += (snum[strIdx] - 0x30) * pow(10, idx);
        }
        strIdx++;
    }

    /* Check flag to see if originally passed -ve number and convert result if so. */
    if(!numIsNeg)
    {
        return accum;
    }
    else
    {
        return accum * -1;
    }
}

void ex_abort( char* message )
{
    printf( "aborted> %s\n",message );
    FILE *err = fopen( "build/out.txt", "ab+" );
    exit( 1 );
}

bool isDigit( char c )
{
    return c <= '9' && c >= '0';
}

bool isBlank( char c )
{
    return c==' '||c=='\t'||c=='\n';
}

bool isOperator( char c )
{
    return c==INCREMENT||c==DECREMENT||c==MULTIPLY||c==DIVIDE||c==POWER;
}

bool isSetter( char c )
{
    return c==SET_0||c==SET_64||c==SET_96||c==SET_A||c==SET_B;
}

bool isOutOpt( char c )
{
    return c==NEW_LINE_OUT||c==SPACE_OUT||c==INT_OUT||c==ASCII_OUT;
}

bool isKnownCharacter( char c )
{
    return isDigit( c ) == true || isOperator( c ) == true
        || isSetter( c ) == true || isOutOpt( c ) == true
        ||c==COMMENT_MARKER||c==INDEX_SPEC||c==COLON||c==L_BRACK
        ||c==L_CURL||c==R_BRACK||c==R_CURL;
}

void process( char *content )
{
    bool forward = true;
    int i = 0;

    int index = -1;
    int values[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };    /* all the values */
                                                        /* one can use */
    int loop_temp = 0;
    int loop_GOTOc = 0;
    int loop_cur = -1;
    int loop_lim = 0;

    int nest_temp = 0;
    int nest_GOTOc = 0;
    int nest_cur = -1;
    int nest_lim = 0;

    bool has_index = false;
    bool is_loop = false;
    bool is_nest = false;

    bool exp_index = false;
    bool exp_temp = false;
    bool exp_nest_temp = false;
    bool exp_colon = false;

    while ( forward == true )
    {
        char token = content[ i ];
        if ( token == '\0' )
        {
            printf( "\n" );
            forward = false;
        }
        else
        {
            if ( is_loop )
            {
                if ( token == R_CURL )
                {
                    if ( loop_cur < loop_lim - 1 )
                    {
                        i = loop_GOTOc;
                        loop_cur++;
                    }
                    else
                    {
                        loop_cur = -1;
                        loop_lim = 0;
                        loop_temp = 0;
                        loop_GOTOc = 0;
                        is_loop = false;
                    }
                }
                else if ( token == L_CURL )
                {
                    ex_abort( "Cannot start basic loop inside another ! "
                        "Please use a nested loop." );
                }
            }
            else if ( !is_loop )
            {
                if ( token == L_CURL )
                {
                    exp_temp = true;
                }
                else if ( token == R_CURL )
                {
                    ex_abort( "No loop to close !" );
                }
            }

            if ( is_nest )
            {
                if ( token == R_BRACK )
                {
                    if ( nest_cur < nest_lim - 1 )
                    {
                        i = nest_GOTOc;
                        nest_cur++;
                    }
                    else
                    {
                        nest_cur = -1;
                        nest_lim = 0;
                        nest_temp = 0;
                        nest_GOTOc = 0;
                        is_nest = false;
                        is_loop = true;
                    }
                }
            }
            else if ( is_loop && !is_nest )
            {
                if ( token == L_BRACK )
                {
                    exp_nest_temp = true;
                }
                else if ( token == R_BRACK )
                {
                    ex_abort( "No nested (inner) loop to close !" );
                }
            }

            if ( isDigit( token ) )
            {
                if ( exp_index )
                {
                    index = token - '0';
                    has_index = true;
                    exp_index = false;
                    if ( !exp_temp )
                    {
                        exp_colon = true;
                    }
                }
                else if ( exp_temp )
                {
                    loop_temp = values[ token - '0' ];
                }
                else if ( exp_nest_temp )
                {
                    nest_temp = values[ token - '0' ];
                }
                else if ( has_index )
                {
                    values[ index ] = values[ token - '0' ];
                }
            }
            else if ( exp_colon )
            {
                if ( token == COLON )
                {
                    exp_colon = false;
                }
                else
                {
                    ex_abort( "Expected colon (':') to be next character !" );
                }
            }
            else if ( token == INDEX_SPEC )
            {
                exp_index = true;
            }
            else if ( exp_index && token == SET_0 )
            {
                for ( int j = 0; j < 10; j++ )
                {
                    values[ j ] = 0;
                }
                exp_colon = true;
            }
            else if ( exp_index && !isDigit( token ) )
            {
                ex_abort( "Expected next character to be a character !" );
            }
            else if ( exp_temp && token == COLON )
            {
                loop_GOTOc = i;
                loop_lim = loop_temp - 1;
                exp_temp = false;
                is_loop = true;
            }
            else if ( exp_nest_temp && token == COLON )
            {
                nest_GOTOc = i;
                nest_lim = nest_temp - 1;
                exp_nest_temp = false;
                is_nest = true;
                is_loop = false;
            }

            if ( isOperator( token ) )
            {
                if ( exp_temp )
                {
                    switch ( token ) {
                        case INCREMENT:
                            loop_temp++;
                            break;
                        case DECREMENT:
                            loop_temp--;
                            break;
                        case MULTIPLY:
                            loop_temp *= 2;
                            break;
                        case DIVIDE:
                            loop_temp = (int) ceil(loop_temp / 2);
                            break;
                        case POWER:
                            loop_temp *= loop_temp;
                            break;
                        default:
                            break;
                    }
                }
                else if ( exp_nest_temp )
                {
                    switch ( token ) {
                        case INCREMENT:
                            nest_temp++;
                            break;
                        case DECREMENT:
                            nest_temp--;
                            break;
                        case MULTIPLY:
                            nest_temp *= 2;
                            break;
                        case DIVIDE:
                            nest_temp = (int) ceil(nest_temp / 2);
                            break;
                        case POWER:
                            nest_temp *= nest_temp;
                            break;
                        default:
                            break;
                    }
                }
                else if ( has_index )
                {
                    switch ( token ) {
                        case INCREMENT:
                            values[ index ]++;
                            break;
                        case DECREMENT:
                            values[ index ]--;
                            break;
                        case MULTIPLY:
                            values[ index ] *= 2;
                            break;
                        case DIVIDE:
                            values[ index ] = (int) ceil(values[ index ] / 2);
                            break;
                        case POWER:
                            values[ index ] *= values[ index ];
                            break;
                        default:
                            break;
                    }
                }
                else
                {
                    switch ( token ) {
                        case INCREMENT:
                            ex_abort( "No viable context for '+' operator !" );
                            break;
                        case DECREMENT:
                            ex_abort( "No viable context for '-' operator !" );
                            break;
                        case MULTIPLY:
                            ex_abort( "No viable context for '*' operator !" );
                            break;
                        case DIVIDE:
                            ex_abort( "No viable context for '/' operator !" );
                            break;
                        case POWER:
                            ex_abort( "No viable context for '*' operator !" );
                            break;
                        default:
                            break;
                    }
                }
            }

            if ( isSetter( token ) )
            {
                if ( exp_temp )
                {
                    switch ( token ) {
                        case SET_0:
                            loop_temp = 0;
                            break;
                        case SET_A:
                            loop_temp = var_a;
                            break;
                        case SET_B:
                            loop_temp = var_b;
                            break;
                        case SET_64:
                            loop_temp = 64;
                            break;
                        case SET_96:
                            loop_temp = 96;
                            break;
                        default:
                            break;
                    }
                }
                else if ( exp_nest_temp )
                {
                    switch ( token ) {
                        case SET_0:
                            nest_temp = 0;
                            break;
                        case SET_A:
                            nest_temp = var_a;
                            break;
                        case SET_B:
                            nest_temp = var_b;
                            break;
                        case SET_64:
                            nest_temp = 64;
                            break;
                        case SET_96:
                            nest_temp = 96;
                            break;
                        default:
                            break;
                    }
                }
                else if ( has_index )
                {
                    switch ( token ) {
                        case SET_0:
                            values[ index ] = 0;
                            break;
                        case SET_A:
                            values[ index ] = var_a;
                            break;
                        case SET_B:
                            values[ index ] = var_b;
                            break;
                        case SET_64:
                            values[ index ] = 64;
                            break;
                        case SET_96:
                            values[ index ] = 96;
                            break;
                        default:
                            break;
                    }
                }
                else
                {
                    ex_abort( "No viable context to set a value." );
                }
            }

            if ( isOutOpt( token ) )
            {
                if ( has_index )
                {
                    switch( token )
                    {
                        case NEW_LINE_OUT:
                            printf( "\n" );
                            break;
                        case SPACE_OUT:
                            printf( " " );
                            break;
                        case INT_OUT:
                            printf( "%d", values[ index ] );
                            break;
                        case ASCII_OUT:
                            printf("%c", (char) (values[ index ] % 128) );
                            break;
                        default:
                            break;
                    }
                }
                else
                {
                    ex_abort( "Illegal location to print out a value or any"
                        " whitespace !" );
                }
            }
        }
        i++;
    }
}


int main ( int argc, char *argv[] )
{
    if ( argc > 4 ) /* argc should be 4 for correct execution */
    {
        /* We print argv[0] assuming it is the program name */
        printf( "usage: %s <filename> [a] [b]", argv[0] );  /* in case of err */
    }
    else
    {
        // We assume argv[1] is the filename to open
        FILE *source = fopen( argv[1], "r" );
        FILE *tmp = fopen( "build/tmp", "ab+" );    /* temp file */

        if ( argc >= 3 ) /* evaluates the 2nd param */
        {
            var_a = to_int( argv[2] );  /* 'a' */
        }

        if ( argc == 4 )    /* evaluates the 3nd param */
        {
            var_b = to_int( argv[3] );  /* 'b' */
        }

        if ( source == 0 )
        {
            printf( "Could not open file : %s\n", argv[1] );
        }
        else
        {
            int x;
            bool is_comment = false;

            /* code opt */
            while  ( ( x = fgetc( source ) ) != EOF )
            {
                if ( !is_comment ) {
                    if ( x == COMMENT_MARKER )
                    {
                        is_comment = true;
                    }
                    else if ( !isBlank( x ) )   /* add only if not blank/comment */
                    {
                        fprintf( tmp, "%c", x );
                    }
                }
                else
                {
                    if ( x == EOL )
                    {
                        is_comment = false;
                    }
                }
            }
            fclose( source );
            fclose( tmp );
            tmp = fopen( "build/tmp", "r" );    /* reopen the opt file */

            char content[MAX_BITFLOW_SIZE] = "";

            if ( tmp != 0 )
            {
                fgets( content, MAX_BITFLOW_SIZE, tmp );
                process( content );     /* does the job */

                /* remove the temp file */
                if( remove( "build/tmp" ) != 0 )
                {
                    printf( "Unable to delete temporary file.\n" );
                }
            }
        }
    }
}
