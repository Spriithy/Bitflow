#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
from sys import *
from math import ceil

at = "@" # indicates the begining of the index positioning statement
nlout = ";" # new line
cln = ":" # indicates the end of the index positioning statement
rst = "!" # sets the current index at 0
cps = "&" # sets the current index at 64 (capital letters ascii position minues one)
ncs = "$" # sets the current index at 96 (non capital letters ascii position minues one)
div = "/" # divides the current index by two
mul = "*" # mutliplies the current index by two
pwr = "^" # returns the current value power 2
inc = "+" # increases the current index by one
dec = "-" # decreases the current index by one
nout = "." # prints the current index value as is (integer)
lout = "," # prints the current index value as an ascii-character
sout = "_" # prints a space
frs = "{" # New loop opening
frd = "}" # Loop closing
wls = "[" # nested loop opening
wld = "]" # nested loop closing

var_a = "a"
var_b = "b"
ARGS = [0, 0]

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
    return tk is rst or tk is cps or tk is ncs or tk is var_a or tk is var_b

def isOperator(tk):
    return tk is div or tk is mul or tk is inc or tk is dec or tk is pwr

def isOutOption(tk):
    return tk is lout or tk is nout or tk is sout or tk is nlout

def isLoopDel(tk):
    return tk is frs or tk is frd

def isLoop2Del(tk):
    return tk is wls or tk is wld

def opt(data):
    content = list(data)
    tokens = []
    tk = ""
    for char in content:
        if char is not "\n" and char is not " " and char is not "\t":
            tk += char
    if tk.startswith('(a,b):{') and tk.endswith('};'):
        content = content[7:-3]
        for char in content:
            if char is not "\n" and char is not " " and char is not "\t":
                tokens.append(char)
    else:
        abort("No main function found ! syntax is : '(a,b):\{ ... \};'")
    return tokens

def parse(content):
    content.append("EOF")
    forward = True
    i = 0

    IDX = -1
    VALUES = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    TMP = 0
    GOTOc = 0
    cur = -1
    lim = 0

    TMP2 = 0
    GOTOc2 = 0
    cur2 = -1
    lim2 = 0

    has_idx = False
    is_loop = False
    is_loop2 = False

    exp_idx = False
    exp_tmp = False
    exp_tmp2 = False
    exp_cln = False

    while forward:
        tk = content[i]
        if tk is "EOF":
            print()
            forward = False

        if is_loop:
            if isLoopDel(tk):
                if tk is frd:
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
            if tk is frs:
                exp_tmp = True
            elif tk is frd:
                abort("No loop to close !")

        if is_loop2:
            if isLoop2Del(tk):
                if tk is wld:
                    if cur2 < lim2 - 1:
                        i = GOTOc2
                        cur2 += 1
                    else:
                        cur2 = -1
                        lim2 = 0
                        TMP2 = 0
                        GOTOc2 = 0
                        is_loop2 = False
                        is_loop = True
        elif is_loop and not is_loop2:
            if tk is wls:
                exp_tmp2 = True
            elif tk is wld:
                abort("No inner loop to close !")

        if isDigit(tk):
            if exp_idx:
                IDX = int(tk)
                has_idx = True
                exp_idx = False
                if not exp_tmp:
                    exp_cln = True
            elif exp_tmp:
                TMP = VALUES[int(tk)]
            elif exp_tmp2:
                TMP2 = VALUES[int(tk)]
            elif has_idx:
                VALUES[IDX] = VALUES[int(tk)]
        elif exp_cln:
            if tk is cln:
                exp_cln = False
            else:
                abort("Cannot find a colon (':') to start process !")
        elif tk is at:
            exp_idx = True
        elif exp_idx and tk is rst:
            VALUES = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
            exp_cln = True
        elif exp_idx and not isDigit(tk):
            abort("Cannot resolve '" + tk + "' as a correct index !")
        elif exp_tmp and tk is cln:
            GOTOc = i
            lim = TMP - 1
            exp_tmp = False
            is_loop = True
        elif exp_tmp2 and tk is cln:
            GOTOc2 = i
            lim2 = TMP2 - 1
            exp_tmp2 = False
            is_loop = False
            is_loop2 = True

        if isOperator(tk):
            if exp_tmp:
                if tk is inc:
                    TMP += 1
                elif tk is dec:
                    TMP -= 1
                elif tk is pwr:
                    TMP *= TMP
                elif tk is div:
                    TMP = ceil(TMP / 2)
                elif tk is mul:
                    TMP *= 2
            elif exp_tmp2:
                if tk is inc:
                    TMP2 += 1
                elif tk is dec:
                    TMP2 -= 1
                elif tk is pwr:
                    TMP2 *= TMP
                elif tk is div:
                    TMP2 = ceil(TMP2 / 2)
                elif tk is mul:
                    TMP2 *= 2
            elif has_idx:
                if tk is inc:
                    VALUES[IDX] += 1
                elif tk is dec:
                    VALUES[IDX] -= 1
                elif tk is pwr:
                    VALUES[IDX] *= VALUES[IDX]
                elif tk is div:
                    VALUES[IDX] = ceil(VALUES[IDX] / 2)
                elif tk is mul:
                    VALUES[IDX] *= 2
            else:
                if tk is inc:
                    abort("No viable context for '+' operator !")
                elif tk is dec:
                    abort("No viable context for '-' operator !")
                elif tk is pwr:
                    abort("No viable context for '^' operator !")
                elif tk is div:
                    abort("No viable context for '/' operator !")
                elif tk is mul:
                    abort("No viable context for '*' operator !")

        if isSetter(tk):
            if tk is rst:
                if exp_tmp:
                    TMP = 0
                elif exp_tmp2:
                    TMP2 = 0
                elif has_idx:
                    VALUES[IDX] = 0
                else:
                    abort("No viable context to reset the value !")
            elif tk is cps:
                if exp_tmp:
                    TMP = 64
                elif exp_tmp2:
                    TMP2 = 64
                elif has_idx:
                    VALUES[IDX] = 64
                else:
                    abort("No viable context to set the value to be 64 !")
            elif tk is ncs:
                if exp_tmp:
                    TMP = 96
                elif exp_tmp2:
                    TMP2 = 96
                elif has_idx:
                    VALUES[IDX] = 96
                else:
                    abort("No viable context to set the value to be 96 !")
            elif tk is var_a:
                if exp_tmp:
                    TMP = ARGS[0]
                elif exp_tmp2:
                    TMP2 = ARGS[0]
                elif has_idx:
                    VALUES[IDX] = ARGS[0]
                else:
                    abort("No viable context to set the value to be 'a' !")
            elif tk is var_b:
                if exp_tmp:
                    TMP = ARGS[1]
                elif exp_tmp2:
                    TMP2 = ARGS[1]
                elif has_idx:
                    VALUES[IDX] = ARGS[1]
                else:
                    abort("No viable context to set the value to be 'b' !")

        if isOutOption(tk):
            if tk is nout:
                if exp_tmp or exp_tmp2:
                    abort("Loop counter definition zone isn't a valid context for printing a value !")
                elif has_idx:
                    print(VALUES[IDX], end="")
                else:
                    print("")
            elif tk is lout:
                if exp_tmp or exp_tmp2:
                    abort("Loop counter definition zone isn't a valid context for printing a value !")
                elif has_idx and VALUES[IDX] > 31:
                    print(chr(VALUES[IDX]), end="")
                else:
                    abort("Invalid value to print as ascii-character (value <= 31), or invalid context !")
            elif tk is sout:
                if not exp_tmp and not exp_tmp2:
                    print("", end=" ")
            elif tk is nlout:
                if not exp_tmp and not exp_tmp2:
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
        try:
            if len(argv) >= 3:
                ARGS[0] = int(argv[2])
            if len(argv) >= 4:
                ARGS[1] = int(argv[3])
        except ValueError:
            abort("Invalid parameters passed to main ! The two parameters must be integers !")
        parse(content)
    else:
        abort("Usage : ./bitflowc <file_name.bitflow>")

run()
