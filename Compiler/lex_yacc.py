import ply.lex as lex
import ply.yacc as yacc
import sys


reserved = {
    'if' : 'K_IF',
    'ef' : 'K_EF',
    'el' : 'K_EL',
    'end' : 'K_END',
    'while' : 'K_WHILE',
    'int' : 'K_INT',
    'double' : 'K_DOUBLE',
    'string' : 'K_STRING',
    'null' : 'K_NULL',
    'list' : 'K_LIST',
    'set' : 'K_SET',
    'dict' : 'K_DICT',
    'Window' : 'K_WINDOW',
    'Triangle' : 'K_TRIANGLE',
    'Circle' : 'K_CIRCLE',
    'Shape' : 'K_SHAPE',
    'Rectangle' : 'K_RECTANGLE',
    'Point' : 'K_POINT',
    'bool' : 'K_BOOL',
    'true' : 'K_TRUE',
    'false' : 'K_FALSE',
    'done' : 'K_DONE',
    'continue' : 'K_CONTINUE'
}


# List of token names.   This is always required
tokens = [   
    'ID',
    'GT',
    'LT',
    'GEQ',
    'LEQ',
    'EQ',
    'NEQ',
    'NEG',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'AND',
    'OR',
    'ASSIGN',
    'LPAREN',
    'RPAREN',   
    'STRING',
    'INTEGER',
    'DOUBLE',
    'COMMA', 
    'COMMENT'
] + list(reserved.values())

# Regular expression rules for simple tokens

t_GT = r'>'
t_LT = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_EQ = r'='
t_NEQ = r'!='
t_NEG = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_AND = r'&&'
t_OR = r'\|\|'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'  
t_STRING = r'\"([^\"]|\\")*\"'

t_COMMA = r','


# A regular expression rule with some action code
def t_INTEGER(t):
    r'(\+|-)?[0-9]+'
    t.value = int(t.value)    
    return t

def t_DOUBLE(t):
    r'(\+|-)?([0-9]\+\.?)'
    t.value = float(t.value)    
    return t

def t_ID(t):
  r'[_a-zA-Z][_a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'/\*(/|(\*)*[^\*])*(\*)+/|//.*'
    return t  

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

indent = 0

def p_program(p):
    """
    program : statement_list
    """
    p[0] = p[1]
    print p[0]


def p_statement_list(p):
    """
    statement_list :
    statement_list : statement_list statement
    """
    #Somehow keep track of indentation
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = p[1] + ("\n" if p[1] else "") + p[2]

def p_statement(p):
    """    
    statement : compound_statement
    """
    p[0] = p[1]


def p_compound_statement(p):
    """
    compound_statement : function_call_statement
    """
    p[0] = p[1]

def p_function_call_statement(p):
    """    
    function_call_statement : ID LPAREN parameter_list RPAREN
    function_call_statement : ID LPAREN RPAREN
    """
    if len(p) == 5:
        p[0] = p[1] + "(" + p[3] + ")"
    else:
        p[0] = p[1] + "()"


def p_parameter_list(p):
    """
    parameter_list : parameter_list COMMA STRING
    parameter_list : STRING
    """
    if len(p) == 4:
        p[0] = p[1] + ", " + p[3]
    else:
        p[0] = p[1]

def p_error(p):
    print "unknown text at " + p.value


parser = yacc.yacc()

while True:
    try:
        expressions = raw_input("> ")
    except EOFError:
        break
    if expressions:
        parser.parse(expressions)






