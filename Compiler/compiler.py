from parser import *
import traceback, sys


p = Parser()

if len(sys.argv) == 2:
    try:
        f = open(sys.argv[1])
        data = f.read()
        p.parser.parse(data)
        flags["function_parsing"] = False
        init_scope_stack()

        #Had to call lex.lex() to restart line counting
        p.lexer.lex()
        sys.stdout.write(p.parser.parse(data))

    except Parse_Error:
        exit(1)
    except :
        traceback.print_exc()
else:
    while True:
        try:
            expressions = raw_input("geo> ")
        except :
            traceback.print_exc()
            continue
        if expressions:
            p.parser.parse(expressions)






