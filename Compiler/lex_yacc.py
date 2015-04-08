import ply.lex as lex
import ply.yacc as yacc
import sys
import traceback

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
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


class ScopeStack:
    def __init__(self):
        self.scopes = []
        self.scopes.append(Scope())

    def add_scope(self):
        new_scope = Scope()
        self.scopes.append(new_scope)
        return new_scope

    def get_current_scope(self):
        assert len(self.scopes) > 0
        return self.scopes[len(self.scopes) - 1]

    def pop_scope(self):
        assert self.scopes > 1
        return self.scopes.pop()

    def get_var(self, id):
        for scope in reversed(self.scopes):
            var = scope.get_var(id)

            if var:
                return var

        return None


class Scope:
    def __init__(self):
        self.vars = {}

    def add_declaration(self, id, type, pre_type=None):
        assert id not in self.vars
        self.vars[id] = {
            'type' : type,
            'pre_type' : pre_type,
            'given_name' : id + '_' + str(len(scope_stack.scopes))
        }

        return self.vars[id]['given_name']

    def get_var(self, id):
        if id in self.vars:
            return self.vars[id]
        return None


class Function:
    def __init__(self, type=None, args=[]):
        self.type = type
        self.args = args


class Production:
    def __init__(self, type=None, text=None, pre_type=None, children=None, production_type=None):
        self.type = type
        self.text = text
        self.pre_type = pre_type
        self.children = children
        self.production_type = production_type

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)



#@todo add builtin functions
functions = {}
scope_stack = ScopeStack()

# Flag set to true to ignore variable declaration checking
flags = {
    "ignore" : False
}


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
    if type(p[1]) is str:
        p[0] = p[1]
    else:
        p[0] = p[1].text


def p_function_call_statement(p):
    """    
    function_call_statement : ID LPAREN parameter_list RPAREN
    function_call_statement : ID LPAREN RPAREN
    """

    type = "unknown"
    text = None

    if p[1] in functions:
        type = functions[p[1]].type

    if len(p) == 5:
        text = p[1] + "(" + p[3] + ")"
        p[0] = Production(type=type, text=text, production_type="function_call") #fix me
    else:
        text = p[1] + "()"
        p[0] = Production(type=type, text=text, production_type="function_call")


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
            var_name = add_variable_declaration(p[3], p[2], p[1])
            p[0] = var_name + " = None"
        elif p[1] == "list":
            var_name = add_variable_declaration(p[3], p[2], p[1])
            p[0] = var_name + " = []"
        elif p[1] == "dict":
            var_name = add_variable_declaration(p[3], p[2], p[1])
            p[0] = var_name + " = {}"
        elif p[1] == "set":
            var_name = add_variable_declaration(p[3], p[2], p[1])
            #@todo Don't know
            p[0] = var_name + " = {}"
        elif p[2] == ":=":
            var_name = p[1]

            if check_var_in_scope(p[1], p):
                var = scope_stack.get_var(p[1])
                var_name = var['given_name']

            p[0] = var_name + " = " + p[3]

    elif len(p) == 6:
        var_name = add_variable_declaration(p[3], p[2], p[1])
        p[0] = var_name + " = " + p[5]


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
    expression_term : expression_term op unary_expression
    expression_term : unary_expression
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
    primary_expression : id_expression
    primary_expression : function_call_statement
    """
    p[0] = p[1]


def p_id_expression(p):
    """
    id_expression : ID
    """

    prod = Production(text=p[1],children=[p[1]], production_type="id")

    if check_var_in_scope(p[1], p):
        var = scope_stack.get_var(p[1])

        prod.text = var['given_name']

        prod.type = var["type"]
        prod.pre_typ = var["pre_type"]

    p[0] = prod


def p_constant(p):
    """
    constant : boolean_constant
    constant : number
    constant : string_constant
    """
    p[1].production_type = "constant"
    p[0] = p[1]


def p_string_constant(p):
    """
    string_constant : STRING
    """
    p[0] = Production(type="string", text=p[1], children=[p[1]])


def p_boolean_constant(p):
    """
    boolean_constant : K_TRUE
    boolean_constant : K_FALSE
    """
    text = ""
    if p[1] == "true":
        text = "True"
    else:
        text = "False"

    p[0] = Production(type="bool", text=text, children=[p[1]])


def p_unary_expression(p):
    """
    unary_expression : LPAREN expression RPAREN
    unary_expression : primary_expression
    """
    if len(p) == 4:
        p[0] = "(" + p[2] + ")"
    else:
        p[0] = p[1].text



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
    p[0] = Production(type="number", text=p[1], children=[p[1]])


def p_selection_statement(p):
    """
    selection_statement :   if_statement \
                            else_if_statement_list \
                            else_statement \
                        K_END
    """
    p[0] = p[1] + ("\n" if p[2] else "") + p[2] + ("\n" if p[3] else "") + p[3]


def p_if_statement(p):
    """
    if_statement : K_IF LPAREN expression RPAREN \
                                push_scope \
                                compound_statement_list \
    """
    p[0] = "if " + p[3] + ":\n" + indent(p[6])
    pop_scope(p)


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
                                push_scope \
                                compound_statement_list
    """
    p[0] = "elif " + p[3] + ":\n" + indent(p[6])
    pop_scope(p)


def p_else_statement(p):
    """
    else_statement :
    else_statement : K_EL push_scope compound_statement_list
    """
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = "else:\n" + indent(p[3])
        pop_scope(p)


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
                            push_scope \
                            compound_statement_list \
                        K_END
    """
    p[0] = "while " + p[3] + ":\n" + indent(p[6])
    pop_scope(p)


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
    function_declaration : function_header \
                                compound_statement_list \
                            K_END
    """
    header = p[1]

    p[0] = header[0] + "\n" + indent(p[2]) + "\n" + indent("return " + header[1])
    pop_scope(p)


def p_function_header(p):
    """
    function_header : pre_type_modifier type ID LPAREN push_scope argument_list RPAREN ASSIGN set_ignore_flag \
                        primary_expression unset_ignore_flag
    function_header : pre_type_modifier type ID LPAREN push_scope RPAREN ASSIGN set_ignore_flag \
                        primary_expression unset_ignore_flag
    """

    if p[3] in functions:
        print_err("Error: redeclaration of function " + p[3], p)

    f = Function(type=p[2])

    text = None
    ret_expression = None
    return_id = None

    if len(p) == 12:
        init_ret = None

        #if not an ID
        ret_expression = p[10].text
        if p[10].production_type == 'id':
            var_name = add_variable_declaration(p[10].text, p[2], p[1])
            init_ret = var_name + " = None"
            ret_expression = var_name

        text = "def " + p[3] + "(" + p[6] + "):" + ("\n" if init_ret else "") + indent(init_ret)
        f.args = p[6]
    else:
        init_ret = None

        #if not an ID
        ret_expression = p[9].text
        if p[9].production_type == 'id':
            var_name = add_variable_declaration(p[9].text, p[2], p[1])
            init_ret = var_name + " = None"
            ret_expression = var_name

        text = "def " + p[3] + "():" + ("\n" if init_ret else "") + indent(init_ret)
        f.args = None


    p[0] = (text, ret_expression)


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
    scope = scope_stack.get_current_scope()

    pre_type = None
    if p[1] != "":
        pre_type = p[1]

    var_name = add_variable_declaration(p[3], p[2], pre_type)
    p[0] = var_name


def p_push_scope(p):
    """
    push_scope :
    """
    p[0] = ""
    scope_stack.add_scope()


def pop_scope(p):
    scope_stack.pop_scope()


def add_variable_declaration(id, type, pre_type=None):
    scope = scope_stack.get_current_scope()
    return scope.add_declaration(id, type, pre_type)


def p_set_ignore_flag(p):
    """
    set_ignore_flag :
    """
    flags['ignore'] = True

    p[0] = ""


def p_unset_ignore_flag(p):
    """
    unset_ignore_flag :
    """
    flags['ignore'] = False
    p[0] = ""


def check_var_in_scope(var, p):
    if flags['ignore']:
        return False

    if not scope_stack.get_var(p[1]):
        print_err("Variable '" + p[1] + "' hasn't been declared", p)
        return False
    
    return True


def indent(p):
    if not p:
        return ""

    ret = []
    for s in p.split("\n"):
        ret.append("    " + s)
    return "\n".join(ret)


def p_error(p):
    print_err("unknown text at " + p.value + ": line no " + str(p.lineno))


def print_err(error, p=None):
    if p:
        error = error + ": " + str(p.lineno(1))

    print >>sys.stderr, error


parser = yacc.yacc()


if len(sys.argv) == 2:
    try:
        f = open(sys.argv[1])
        data = f.read()
        parser.parse(data)
    except:
        traceback.print_exc()
else:
    while True:
        try:
            expressions = raw_input("geo> ")
        except :
            print sys.exc_info()[0]
            continue
        if expressions:
            parser.parse(expressions)






