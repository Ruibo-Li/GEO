#!/usr/bin/python

import lex, yacc

#################### Lex Tokenizer ####################

# List of tokens
tokens = ("INTEGER", "PLUS", "MINUS", "TIMES", "DIVIDE", "NEGATE", "NEWLINE")

# Regular expressions for the above tokens (except INTEGER)
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_NEGATE = r"~"
t_NEWLINE = r"\\n"

# Ignore spaces and tabs
t_ignore = " \t"

# Regular expression for INTEGER and convert the integer to an int type
def t_INTEGER(t):
    r"(\+|-)?[0-9]+"
    # Return the token as an int type
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large %d" % t.value
        t.value = 0
    return t

# Define lexical error
def t_error(t):
    print "Illegal character %s" % t.value[0]
    t.lexer.skip(1)

# Construct tokenizer using Lex
lex.lex()


#################### Yacc Parser ####################

# Context free grammar for an input line
def p_line(p):
    """line : line expression NEWLINE
            | line NEWLINE
            | empty """
    if len(p) == 4:
        print p[2]

# Context free grammar for epsilon
def p_empty(p):
    "empty : "
    pass

# Context free grammar for expression
def p_expression(p):
    """expression : addition
                  | subtraction
                  | multiplication
                  | division
                  | negation
                  | INTEGER """
    p[0] = p[1]

# Context free grammar for addition
def p_expression_plus(p):
    "addition : PLUS expression expression"
    p[0] = p[2] + p[3]

# Context free grammar for subtraction
def p_expression_minus(p):
    "subtraction : MINUS expression expression"
    p[0] = p[2] - p[3]

# Context free grammar for multiplication
def p_expression_times(p):
    "multiplication : TIMES expression expression"
    p[0] = p[2] * p[3]

# Context free grammar for division
def p_expression_division(p):
    "division : DIVIDE expression expression"
    p[0] = p[2] / p[3]

# Context free grammar for negation
def p_expression_negation(p):
    "negation : NEGATE expression"
    p[0] = -p[2]

# Catch syntax error
def p_error(p):
    print "Syntax error"

# Construct parser using Yacc
parser = yacc.yacc()


#################### Parse and Calculate ####################
while True:
    try:
        expressions = raw_input("> ")
    except EOFError:
        break
    if expressions:
        parser.parse(expressions)