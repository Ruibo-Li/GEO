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

        program = p.parser.parse(data)

        print "import sys"
        print "import os.path"
        print "sys.path.append(os.path.join(os.path.dirname(__file__), '..'))"
        print "from Built_in_Functions.built_in import *"

        sys.stdout.write(program)

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






