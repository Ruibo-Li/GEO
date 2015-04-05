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
    'continue' : 'K_CONTINUE',
    'break' : 'K_BREAK'
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
#    return t

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
    statement : function_declaration
    statement : compound_statement
    """
    p[0] = p[1]


def p_compound_statement(p):
    """
    compound_statement : function_call_statement
    compound_statement : variable_declaration
    compound_statement : selection_statement
    compound_statement : iteration_statement
    compound_statement : jump_statement
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
    type : K_POINT
    type : K_TEXT
    """
    p[0] = p[1]


def p_expression(p):
    """
    expression : expression op expression_term
    expression : expression_term
    """
    p[0] = p[1]


def p_expression_term(p):
    """
    expression_term : expression_term op primary_expression
    expression_term : primary_expression
    """
    if len(p) == 4:
        p[0] = p[1] + " " + p[2] + " " + p[3]
    else:
        p[0] = p[1]


def p_op(p):
    """
    op : PLUS
    op : MINUS
    op : TIMES
    op : DIVIDE
    op : MOD
    op : comparator
    op : boolean_operator
    """
    p[0] = p[1]

def p_boolean_operator(p):
    """
    boolean_operator : AND
    boolean_operator : OR
    """
    if p[1] == "&&":
        p[0] = "and"
    else:
        p[0] = "or"

def p_primary_expression(p):
    """
    primary_expression : constant
    primary_expression : ID
    primary_expression : function_call_statement
    primary_expression : LPAREN expression RPAREN
    """
    if len(p) == 4:
        p[0] = "(" + p[2] + ")"
    else:
        p[0] = p[1]

def p_constant(p):
    """
    constant : boolean_constant
    constant : number
    constant : STRING
    """
    p[0] = p[1]


def p_boolean_constant(p):
    """
    boolean_constant : K_TRUE
    boolean_constant : K_FALSE
    """
    if p[1] == "true":
        p[0] = "True"
    else:
        p[0] = "False"


def p_unary_expression(p):
    """
    unary_expression : primary_expression
    """
    p[0] = p[1]



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


def p_number(p):
    """
    number : INTEGER
    number : DOUBLE
    """
    p[0] = p[1]



def p_selection_statement(p):
    """
    selection_statement : K_IF LPAREN expression RPAREN \
                                compound_statement_list \
                            else_if_statement_list \
                            else_statement \
                        K_END
    """
    p[0] = "if " + p[3] + ":\n" +indent(p[5])+ ("\n" if p[6] else "") + p[6] + ("\n" if p[7] else "") + p[7]

def p_else_if_statement_list(p):
    """
    else_if_statement_list :
    else_if_statement_list : else_if_statement_list else_if_statement
    """
    if len(p) == 1:
        p[0] = ""
    else:
        if p[1] == "":
            p[0] = p[2]
        else:
            p[0] = p[1] + "\n" + p[2]



def p_else_if_statement(p):
    """
    else_if_statement : K_EF LPAREN expression RPAREN \
                                compound_statement_list
    """
    p[0] = "elif " + p[3] + ":\n" + indent(p[5])


def p_else_statement(p):
    """
    else_statement :
    else_statement : K_EL compound_statement_list
    """
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = "else:\n" + indent(p[2])

def p_compound_statement_list(p):
    """
    compound_statement_list :
    compound_statement_list : compound_statement_list compound_statement
    """
    if len(p) == 1:
        p[0] = ""
    else:
        if p[1] == "":
            p[0] = p[2]
        else:
            # @todo indent
            p[0] = p[1] + "\n" + p[2]


def p_iteration_statement(p):
    """
    iteration_statement : K_WHILE LPAREN expression RPAREN \
                            compound_statement_list \
                        K_END
    """
    p[0] = "while " + p[3] + ":\n" + indent(p[5])


def p_jump_statement(p):
    """
    jump_statement : K_CONTINUE
    jump_statement : K_BREAK
    jump_statement : K_DONE
    """
    if p[1] == "done":
        p[0] = "return"
    elif p[1] == "break":
        p[0] = "break"
    else:
        p[0] = "continue"


def p_function_declaration(p):
    """
    function_declaration : pre_type_modifier type ID LPAREN argument_list RPAREN ASSIGN unary_expression \
                                compound_statement_list \
                            K_END
    function_declaration : pre_type_modifier type ID LPAREN RPAREN ASSIGN unary_expression \
                                compound_statement_list \
                            K_END
    """
    if len(p) == 11:
        p[0] = "def " + p[3] + "(" + p[5] + "):\n" + indent(p[8]) + " = None\n" + indent(p[9]) + "\n" + indent("return " + p[8])
    else:
        p[0] = "def " + p[3] + "():\n" + indent(p[7]) + " = None\n" + indent(p[8]) + "\n" + indent("return " + p[7])


def p_argument_list(p):
    """
    argument_list : argument_list COMMA argument
    argument_list : argument
    """
    if len(p) == 4:
        p[0] = p[1] + ", " + p[3]
    else:
        p[0] = p[1]


def p_argument(p):
    """
    argument : pre_type_modifier type ID
    """
    p[0] = p[3]

def indent(p):
    ret = []
    for s in p.split("\n"):
        ret.append("    " + s)
    return "\n".join(ret)

def p_error(p):
    print_err("unknown text at " + p.value)

def print_err(error):
    print >>sys.stderr, error

parser = yacc.yacc()


if len(sys.argv) == 2:
    try:
        f = open(sys.argv[1])
        data = f.read()
        parser.parse(data)
    except:
        print_err(sys.exc_info()[0])
else:
    while True:
        try:
            expressions = raw_input("> ")
        except :
            print sys.exc_info()[0]
            continue
        if expressions:
            parser.parse(expressions)






