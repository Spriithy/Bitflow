#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
from sys import *
from math import ceil

at = "@" # indicates the begining of the index positioning statement
sp = "#" # exits current index context
nlout = ";" # new line
cln = ":" # indicates the end of the index positioning statement
rst = "!" # sets the current index at 0
cps = "&" # sets the current index at 64 (capital letters ascii position minues one)
ncs = "$" # sets the current index at 96 (non capital letters ascii position minues one)
div = "/" # divides the current index by two
mul = "*" # mutliplies the current index by two
inc = "+" # increases the current index by one
dec = "-" # decreases the current index by one
nout = "." # prints the current index value as is (integer)
lout = ">" # prints the current index value as an ascii-character
sout = "_" # prints a space
lst = "{" # New loop opening
lnd = "}" # Loop closing

pn1 = "x"
pn2 = "y"
pn3 = "z"
prs = "("
prl = ","
prd = ")"



def abort(msg):
    print("aborted > " + msg)
    exit()

def isDigit(tk):
    try:
        i = int(tk)
        return True
    except ValueError:
        return False

def isSetter(tk):
    return tk is rst or tk is cps or tk is ncs

def isOperator(tk):
    return tk is div or tk is mul or tk is inc or tk is dec

def isOutOption(tk):
    return tk is lout or tk is nout or tk is sout or tk is nlout

def isLoopDel(tk):
    return tk is lst or tk is lnd

def opt(data):
    content = list(data)
    tk = []
    for char in content:
        if char is not "\n" and char is not " " and char is not "\t":
            tk.append(char)
    return tk

def parse(content):
    content.append(";")
    content.append("EOF")
    forward = True
    i = 0

    IDX = -1
    VALUES = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    TMP = 0
    GOTOc = 0
    cur = -1
    lim = 0

    has_idx = False
    is_loop = False

    exp_idx = False
    exp_tmp = False
    exp_cln = False

    while forward:
        tk = content[i]

        if tk is "EOF":
            forward = False

        if is_loop:
            if isLoopDel(tk):
                if tk is lnd:
                    if cur < lim - 1:
                        i = GOTOc
                        cur += 1
                    else:
                        cur = -1
                        lim = 0
                        TMP = 0
                        GOTOc = 0
                        is_loop = False
        else:
            if tk is lst:
                exp_tmp = True
            elif tk is lnd:
                abort("No loop to close !")

        if isDigit(tk):
            if exp_idx:
                IDX = int(tk)
                has_idx = True
                exp_idx = False
                if not exp_tmp:
                    exp_cln = True
            elif exp_tmp:
                TMP = VALUES[int(tk)]
            elif has_idx:
                VALUES[IDX] = VALUES[int(tk)]
        elif exp_cln:
            if tk is cln:
                exp_cln = False
            else:
                abort("Cannot find a colon (':') to start process !")
        elif tk is at:
            exp_idx = True
        elif exp_idx and not isDigit(tk):
            abort("Cannot resolve '" + tk + "' as a correct index !")
        elif exp_tmp and tk is cln:
            GOTOc = i
            lim = TMP - 1
            exp_tmp = False
            is_loop = True
        elif tk is sp:
            has_idx = False

        if isOperator(tk):
            if tk is inc:
                if exp_tmp:
                    TMP += 1
                elif has_idx:
                    VALUES[IDX] += 1
                else:
                    abort("No viable context for '+' operator !")
            elif tk is dec:
                if exp_tmp:
                    TMP -= 1
                elif has_idx:
                    VALUES[IDX] -= 1
                else:
                    abort("No viable context for '-' operator !")
            elif tk is div:
                if exp_tmp:
                    TMP = ceil(TMP / 2)
                elif has_idx:
                    VALUES[IDX] = ceil(VALUES[IDX] / 2)
                else:
                    abort("No viable context for '/' operator !")
            elif tk is mul:
                if exp_tmp:
                    TMP *= 2
                elif has_idx:
                    VALUES[IDX] *= 2
                else:
                    abort("No viable context for '*' operator !")

        if isSetter(tk):
            if tk is rst:
                if exp_tmp:
                    TMP = 0
                elif has_idx:
                    VALUES[IDX] = 0
                else:
                    abort("No viable context to reset the value !")
            elif tk is cps:
                if exp_tmp:
                    TMP = 64
                elif has_idx:
                    VALUES[IDX] = 64
                else:
                    abort("No viable context to set the value to be 64 !")
            elif tk is ncs:
                if exp_tmp:
                    TMP = 96
                elif has_idx:
                    VALUES[IDX] = 96
                else:
                    abort("No viable context to set the value to be 96 !")

        if isOutOption(tk):
            if tk is nout:
                if exp_tmp:
                    abort("Loop counter definition zone isn't a valid context for printing a value !")
                elif has_idx:
                    print(VALUES[IDX], end="")
                else:
                    print("")
            elif tk is lout:
                if exp_tmp:
                    abort("Loop counter definition zone isn't a valid context for printing a value !")
                elif has_idx and VALUES[IDX] > 31:
                    print(chr(VALUES[IDX]), end="")
                else:
                    abort("Invalid value to print as ascii-character (value <= 31), or invalid context !")
            elif tk is sout:
                print("", end=" ")
            elif tk is nlout:
                print("")

        i += 1

def run ():
    if len(argv) is 1:
        abort("You must specify a .bitflow file to compile !")
    elif argv[1].split(".")[1] is not "bitflow":
        try:
            data = open(argv[1], "r").read()
        except IOError:
            abort("Cannot open file '" + argv[1] + "' in new file stream !")
        content = opt(data)
        parse(content)
    else:
        abort("Usage : ./bitflowc <file_name.bitflow>")

run()
