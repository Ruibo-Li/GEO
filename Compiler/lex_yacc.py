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
    'Text' : 'K_TEXT',
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
t_INTEGER = r'[0-9]+'
t_DOUBLE = r'[0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+'
t_COMMA = r','


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
    compound_statement : variable_declaration
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
    parameter_list : parameter_list COMMA expression
    parameter_list : expression
    """
    if len(p) == 4:
        p[0] = p[1] + ", " + p[3]
    else:
        p[0] = p[1]

def p_variable_declaration(p):
    """
    variable_declaration : pre_type_modifier type ID
    variable_declaration : pre_type_modifier type ID ASSIGN expression
    variable_declaration : ID ASSIGN expression
    """
    #@todo add all information about var. Process type modifier
    if len(p) == 4:
        if p[1] == "":
            p[0] = p[3] + " = None"
        elif p[1] == "list":
            p[0] = p[3] + " = []"
        elif p[1] == "dict":
            p[0] = p[3] + " = {}"
        elif p[1] == "set":
            #@todo Don't know
            p[0] = p[3] + " = @TODO initialize me"
        elif p[2] == ":=":
            p[0] = p[1] + " = " + p[3]
    elif len(p) == 6:
        #@todo assign value
        p[0] = p[3] + " = " + p[5]

def p_pre_type_modifier(p):
    """
    pre_type_modifier :
    pre_type_modifier : K_LIST
    pre_type_modifier : K_DICT
    pre_type_modifier : K_SET
    """
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = p[1]

def p_type(p):
    """
    type : K_INT
    type : K_DOUBLE
    type : K_STRING
    type : K_BOOL
    type : K_WINDOW
    type : K_SHAPE
    type : K_TRIANGLE
    type : K_RECTANGLE
    type : K_CIRCLE
    type : K_TEXT
    """
    p[0] = p[1]


def p_expression(p):
    """
    expression : string_expression
    expression : unary_expression
    expression : boolean_expression
    expression : arithmetic_expression
    """
    p[0] = p[1]

def p_string_expression(p):
    """
    string_expression : string_expression PLUS string_term
    string_expression : STRING
    """
    if len(p) == 4:
        p[0] = p[1] + " + " + p[3]
    else:
        p[0] = p[1]


def p_string_term(p):
    """
    string_term : function_call_statement
    string_term : STRING
    """
    p[0] = p[1]


def p_unary_expression(p):
    """
    unary_expression : ID
    unary_expression : STRING
    unary_expression : INTEGER
    unary_expression : function_call_statement
    unary_expression : DOUBLE
    unary_expression : K_TRUE
    unary_expression : K_FALSE
    """
    if p[1] == "true":
        p[0] = "True"
    elif p[1] == "false":
        p[0] = "False"
    else:
        p[0] = p[1]

def p_boolean_expression(p):
    """
    boolean_expression : boolean_expression OR boolean_term
    boolean_expression : boolean_term
    """
    if len(p) == 4:
        p[0] = p[1] + " or " + p[3]
    else:
        p[0] = p[1]

def p_boolean_term(p):
    """
    boolean_term : boolean_term AND boolean_factor
    boolean_term : boolean_factor
    """
    if len(p) == 4:
        p[0] = p[1] + " and " + p[3]
    else:
        p[0] = p[1]

def p_boolean_factor(p):
    """
    boolean_factor : LPAREN boolean_expression RPAREN
    boolean_factor : unary_expression comparator unary_expression
    boolean_factor : arithmetic_expression comparator arithmetic_expression
    boolean_factor : string_expression comparator string_expression
    boolean_factor : unary_expression
    boolean_factor : NEG boolean_factor
    """
    if len(p) == 4:
        if p[1] == "(":
            p[0] = "(" + p[2] + ")"
        else:
            p[0] = p[1] + " " + p[2] + " " + p[3]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = " not " + p[2]


def p_comparator(p):
    """
    comparator : GT
    comparator : LT
    comparator : GEQ
    comparator : LEQ
    comparator : EQ
    comparator : NEQ
    """
    if p[1] == '=':
        p[0] = "=="
    else:
        p[0] = p[1]


def p_arithmetic_expression(p):
    """
    arithmetic_expression : arithmetic_expression PLUS arithmetic_term
    arithmetic_expression : arithmetic_expression MINUS arithmetic_term
    arithmetic_expression : arithmetic_term
    """
    if len(p) == 4:
        if p[2] == "+":
            p[0] = p[1] + " + " + p[3]
        else:
            p[0] = p[1] + " - " + p[3]
    else:
        p[0] = p[1]



def p_arithmetic_term(p):
    """
    arithmetic_term : arithmetic_term TIMES arithmetic_factor
    arithmetic_term : arithmetic_term DIVIDE arithmetic_factor
    arithmetic_term : arithmetic_term MOD arithmetic_factor
    arithmetic_term : arithmetic_factor
    """
    if len(p) == 4:
        if p[2] == "*":
            p[0] = p[1] + " * " + p[3]
        elif p[2] == "/":
            p[0] = p[1] + " / " + p[3]
        else:
            p[0] = p[1] + " % " + p[3]
    else:
        p[0] = p[1]


def p_arithmetic_factor(p):
    """
    arithmetic_factor : LPAREN arithmetic_expression RPAREN
    arithmetic_factor : number
    arithmetic_factor : function_call_statement
    arithmetic_factor : MINUS arithmetic_factor
    """
    if len(p) == 4:
        p[0] = "(" + p[2] + ")"
    elif len(p) == 3:
        p[0] = "-" + p[2]
    else:
        p[0] = p[1]


def p_number(p):
    """
    number : INTEGER
    number : DOUBLE
    """
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






