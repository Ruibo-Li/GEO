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
t_DOUBLE = r'[0-9]+\.[0-9]*|[0-9]*\.[0-9]+'
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

    def add_declaration(self, id, type, pre_type=None, global_var=False):
        #@todo add line number to error by saving it with the var
        if id in self.vars:
            print_err("Variable '" + id + "' was already declared")

        self.vars[id] = {
            'type' : type,
            'pre_type' : pre_type,
            'given_name' : id + '_' + str(len(scope_stack.scopes)),
            'global_var' : global_var
        }

        return self.vars[id]['given_name']

    def get_var(self, id):
        if id in self.vars:
            return self.vars[id]
        return None


class Function:
    def __init__(self, type=None, name=None, args=[]):
        self.type = type
        self.args = args
        self.name = name

    def __str__(self):
        return "(type=" + self.type +", args=" + str(self.args) + ", name=" + self.name + ")"

    def __repr__(self):
        return str(self)


class Production:
    def __init__(self, type=None, text=None, pre_type=None, children=None, production_type=None):
        self.type = type
        self.text = text
        self.pre_type = pre_type
        self.children = children
        self.production_type = production_type

    def __str__(self):
        return "(text=" + self.text + ", type=" + str(self.type) + ", pre_type=" + str(self.pre_type) + ")"

    def __repr__(self):
        return str(self)


class Parse_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#@todo add builtin functions
functions = {
    "print" : Function(type="unsassignable", args=[{"type" : "string", "pre_type": None}], name="print"),
    "str" : Function(type="string", args=[{"type" : "any", "pre_type": None}], name="str")
}
scope_stack = ScopeStack()

# Flag set to true to ignore variable declaration checking
flags = {
    "ignore" : False,
    "function_parsing" : True,
    "in_function" : False,
    "in_while" : 0, #nested whiles
    "return_expression" : None
}

numbers_list = [
    "int",
    "double"
]


def p_program(p):
    """
    program : statement_list
    """
    p[0] = p[1]


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
    if in_function_parsing_phase():
        p[0] = ""
        return

    if type(p[1]) is str:
        p[0] = p[1]
    else:
        p[0] = p[1].text


def p_function_call_statement(p):
    """    
    function_call_statement : ID LPAREN parameter_list RPAREN
    function_call_statement : ID LPAREN RPAREN
    """

    if in_function_parsing_phase():
        p[0] = ""
        return

    type = "unknown"
    text = None

    if p[1] in functions:
        type = functions[p[1]].type

    if len(p) == 5:
        #@todo check param types
        param_list = [arg[0] for arg in p[3]]
        args_text = ", ".join(param_list)

        text = p[1] + "(" + args_text + ")"
        p[0] = Production(type=type, text=text, production_type="function_call") #fix me
    else:
        text = p[1] + "()"
        p[0] = Production(type=type, text=text, production_type="function_call")


def p_parameter_list(p):
    """
    parameter_list : parameter_list COMMA expression
    parameter_list : expression
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        p[0] = p[1] + [(p[3].text, p[3].type, p[3].pre_type)]
    else:
        p[0] = [(p[1].text, p[1].type, p[1].pre_type)]



def p_variable_declaration(p):
    """
    variable_declaration : pre_type_modifier type ID
    variable_declaration : pre_type_modifier type ID ASSIGN expression
    variable_declaration : ID ASSIGN expression
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    #@todo add all information about var. Process type modifier

    if len(p) == 4:
        if p[1] == "":
            var_name = add_variable_declaration(p[3], p[2], p[1])

            initializer = get_initializer(p[2])

            p[0] = var_name + " = " + initializer
        elif p[1] == "list":
            var_name = add_variable_declaration(p[3], p[2], p[1])
            p[0] = var_name + " = []"

        #Assignment (No declaration)
        elif p[2] == ":=":
            var_name = p[1]

            pre_global_definition = ""

            assign_expr = p[3].text

            if check_var_in_scope(p[1], p):
                var = scope_stack.get_var(p[1])
                var_name = var["given_name"]

                if var["global_var"] and flags["in_function"]:
                    pre_global_definition = "global " + var_name + "\n"

                if var["type"] != p[3].type and var["type"] in numbers_list and p[3].type in numbers_list:
                    if var["type"] == "double":
                        assign_expr = "float(" + assign_expr + ")"
                    else:
                        assign_expr = "int(" + assign_expr + ")"

                #@todo pre_type checking
                elif var["type"] != p[3].type:
                    print_err("Invalid assignment: Trying to assign \"" + p[3].type + "\" to variable of type " + var["type"], p)

            p[0] = pre_global_definition + var_name + " = " + assign_expr

    # Declaration and assignment
    elif len(p) == 6:
        var_name = add_variable_declaration(p[3], p[2], p[1])
        assign_expr = p[5].text

        if p[2] != p[5].type and p[2] in numbers_list and p[5].type in numbers_list:
            if p[2] == "double":
                assign_expr = "float(" + assign_expr + ")"
            else:
                assign_expr = "int(" + assign_expr + ")"

        #@todo pre_type checking
        elif p[2] != p[5].type:
            print_err("Invalid assignment: Trying to assign \"" + p[5].type + "\" to variable of type " + p[2], p)

        p[0] = var_name + " = " + assign_expr


def p_pre_type_modifier(p):
    """
    pre_type_modifier :
    pre_type_modifier : K_LIST
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
    expression : expression boolean_operator expression_pre_term
    expression : expression_pre_term
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        expr = Production()

        if p[1].type == "bool" and p[3].type == "bool":
            expr.type = "bool"
        else:
            print_err("\"" + p[2] + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

        expr.text = p[1].text + " " + p[2] + " " + p[3].text
        expr.children = [p[1], p[2], p[3]]
        p[0] = expr

    else:
        p[0] = p[1]


def p_expression_pre_term(p):
    """
    expression_pre_term : expression_pre_term eq_comparator expression_term
    expression_pre_term : expression_term
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        expr_term = Production()

        op = p[2]

        if op == "=" or op == "!=":
            if p[1].type in numbers_list and p[3].type in numbers_list:
                expr_term.type = "bool"
            elif p[1].type == "string" and p[3].type == "string":
                expr_term.type = "bool"
            elif p[1].type == "bool" and p[3].type == "bool":
                expr_term.type = "bool"
            else:
                print_err("\"" + op + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

        expr_term.text = p[1].text + " " + op + " " + p[3].text
        expr_term.children = [p[1], p[2], p[3]]

        p[0] = expr_term
    else:
        p[0] = p[1]


def p_expression_term(p):
    """
    expression_term : expression_term comparator expression_factor
    expression_term : expression_factor
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        expr_term = Production()

        op = p[2]

        if op == "<" or op == "<=" or op == ">" or op == ">=":
            if p[1].type in numbers_list and p[3].type in numbers_list:
                expr_term.type = "bool"
            elif p[1].type == "string" and p[3].type == "string":
                expr_term.type = "bool"
            elif p[1].type == "bool" and p[3].type == "bool":
                expr_term.type = "bool"
            else:
                print_err("\"" + op + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

        expr_term.text = "(" + p[1].text + " " + op + " " + p[3].text + ")"
        expr_term.children = [p[1], p[2], p[3]]

        p[0] = expr_term
    else:
        p[0] = p[1]


def p_expression_factor(p):
    """
    expression_factor : expression_factor op unary_expression
    expression_factor : unary_expression
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        expr_factor = Production()

        op = p[2]

        #@todo no number type. Change to double or int
        if op == "+":
            if p[1].type in numbers_list and p[3].type in numbers_list:
                if p[1].type == p[3].type:
                    expr_factor.type = p[3].type
                else:
                    expr_factor.type = "double"
            elif p[1].type == "string" and p[3].type == "string":
                expr_factor.type = "string"
            else:
                print_err("\"" + op + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

        elif op == "-" or op == "/" or op == "*" or op == "%":
             if p[1].type in numbers_list and p[3].type in numbers_list:
                if p[1].type == p[3].type:
                    expr_factor.type = p[3].type
                else:
                    expr_factor.type = "double"
             else:
                 print_err("\"" + op + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

        expr_factor.text = p[1].text + " " + p[2] + " " + p[3].text
        expr_factor.children = [p[1], p[2], p[3]]

        p[0] = expr_factor
    else:
        p[0] = p[1]


def p_op(p):
    """
    op : PLUS
    op : MINUS
    op : TIMES
    op : DIVIDE
    op : MOD
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
    primary_expression : MINUS primary_expression
    """
    #@todo type checking
    if len(p) == 3:
        if p[2].type in numbers_list:
            p[2].text = "-" + p[2].text
            p[0] = p[2]
        else:
            print_err("Unary \"-\" can only be used to denote negative integers", p)
            p[0] = p[2]
    else:
        p[0] = p[1]


def p_id_expression(p):
    """
    id_expression : ID
    """

    prod = Production(text=p[1],children=[p[1]], production_type="id")

    check_result = check_var_in_scope(p[1], p)

    if check_result == 1:
        var = scope_stack.get_var(p[1])
        prod.text = var['given_name']

        prod.type = var["type"]
        prod.pre_typ = var["pre_type"]
    elif check_result == 2: #Variable is assigned as return value of function. Ignoreflag is true
        pass
    else:
        print_err("Variable \"" + p[1] + "\" used before declared", p)

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
    unary_expression : NEG primary_expression
    unary_expression : NEG LPAREN expression RPAREN
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if len(p) == 4:
        p[2].text = "(" + p[2].text + ")"
        p[0] = p[2]
    elif len(p) == 3:
        if p[2].type == "bool":
            p[2].text = " not " + p[2].text
            p[0] = p[2]
        else:
            print_err("\"!\" operator can only be used with boolean expressions", p)
    elif len(p) == 5:
        if p[3].type == "bool":
            p[3].text = " not (" + p[3].text + ")"
            p[0] = p[3]
        else:
            print_err("\"!\" operator can only be used with boolean expressions", p)
    else:
        p[0] = p[1]


def p_comparator(p):
    """
    comparator : GT
    comparator : LT
    comparator : GEQ
    comparator : LEQ
    """
    p[0] = p[1]


def p_eq_comparator(p):
    """
    eq_comparator : EQ
    eq_comparator : NEQ
    """
    p[0] = p[1]

def p_number(p):
    """
    number : integer_number
    number : double_number
    """
    p[0] = p[1]


def p_integer_number(p):
    """
    integer_number : INTEGER
    """
    p[0] = Production(type="int", text=p[1], children=[p[1]])


def p_double_number(p):
    """
    double_number : DOUBLE
    """
    p[0] = Production(type="double", text=p[1], children=[p[1]])

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
    if in_function_parsing_phase():
        p[0] = ""
        return


    #@todo make sure it's bool
    p[0] = "if " + p[3].text + ":\n" + indent(p[6])
    pop_scope(p)


def p_else_if_statement_list(p):
    """
    else_if_statement_list :
    else_if_statement_list : else_if_statement_list else_if_statement
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

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

    if in_function_parsing_phase():
        p[0] = ""
        return

    #@todo ensure boolean
    p[0] = "elif " + p[3].text + ":\n" + indent(p[6])
    pop_scope(p)


def p_else_statement(p):
    """
    else_statement :
    else_statement : K_EL push_scope compound_statement_list
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

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
    iteration_statement : iteration_statement_header \
                            compound_statement_list \
                        K_END
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    p[0] = p[1] + ":\n" + indent(p[2])
    pop_scope(p)
    flags["in_while"] -= 1


def p_iteration_statement_header(p):
    """
    iteration_statement_header : K_WHILE LPAREN expression RPAREN
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    #@todo check is boolean expression
    p[0] = "while " + p[3].text
    flags["in_while"] += 1
    push_scope(p)


def p_jump_statement(p):
    """
    jump_statement : K_CONTINUE
    jump_statement : K_BREAK
    jump_statement : K_DONE
    """
    if in_function_parsing_phase():
        p[0] = ""
        return

    if p[1] == "done":
        if flags["in_function"]:
            p[0] = "return " + flags["return_expression"]
        else:
            #@todo Don't know if this should go here or not
            p[0] = ""
            print_err("\"" + p[1] + "\"" + " can only be used inside a function", p)

    elif p[1] == "break":
        if flags["in_while"] > 0:
            p[0] = "break"
        else:
            p[0] = ""
            print_err("\"" + p[1] + "\"" + " can only be used inside a while loop", p)
    else:
        if flags["in_while"] > 0:
            p[0] = "continue"
        else:
            p[0] = ""
            print_err("\"" + p[1] + "\"" + " can only be used inside a while loop", p)


def p_function_declaration(p):
    """
    function_declaration : function_header \
                                compound_statement_list \
                            K_END
    """
    header = p[1]

    p[0] = header[0] + "\n" + indent(p[2]) + "\n" + indent("return " + header[1])
    pop_scope(p)

    flags["in_function"] = False
    flags["return_expression"] = None

    if in_function_parsing_phase():
        p[0] = ""


def p_function_header(p):
    """
    function_header : pre_type_modifier type ID LPAREN push_scope argument_list RPAREN ASSIGN set_ignore_flag \
                        primary_expression unset_ignore_flag
    function_header : pre_type_modifier type ID LPAREN push_scope RPAREN ASSIGN set_ignore_flag \
                        primary_expression unset_ignore_flag
    """

    if in_function_parsing_phase() and p[3] in functions:
        print_err("Error: redeclaration of function " + p[3], p)

    f = Function(type=p[2], name=p[3])


    text = None
    ret_expression = None
    return_id = None

    if in_function_parsing_phase():
        if p[3] in functions:
            print_err("Redeclaration of function \"" + p[3] + "\"", p, True)

    if len(p) == 12:
        init_ret = None

        arg_list = [arg[0] for arg in p[6]]
        args_text = ", ".join(arg_list)

        #if not an ID
        ret_expression = p[10].text
        if p[10].production_type == 'id':
            if not check_variable_in_current_scope(p[10].text):
                var_name = add_variable_declaration(p[10].text, p[2], p[1])

                initializer = get_initializer(p[2])

                init_ret = var_name + " = " + initializer
                ret_expression = var_name

            # check to make sure the argument has the same type
            else:
                var = scope_stack.get_var(p[10].text)
                arg = [arg for arg in p[6] if arg[0] == var["given_name"]][0]

                if arg[1] != p[2]:
                    print_err("Argument '" + p[10].text + "' doesn't match the type of the function", p)

                ret_expression = var['given_name']

        if in_function_parsing_phase():
            args = []
            for arg in p[6]:
                args.append({
                    "type" : arg[1],
                    "pre_type" : arg[2]
                })
            f.args = args

        text = "def " + p[3] + "(" + args_text + "):" + ("\n" if init_ret else "") + indent(init_ret)
    else:
        init_ret = None

        #if not an ID
        ret_expression = p[9].text
        if p[9].production_type == 'id':
            var_name = add_variable_declaration(p[9].text, p[2], p[1])

            initializer = get_initializer(p[2])

            init_ret = var_name + " = " + initializer
            ret_expression = var_name

        text = "def " + p[3] + "():" + ("\n" if init_ret else "") + indent(init_ret)

    flags["in_function"] = True
    flags["return_expression"] = ret_expression

    p[0] = (text, ret_expression)

    if in_function_parsing_phase():
        functions[p[3]] = f


def p_argument_list(p):
    """
    argument_list : argument_list COMMA argument
    argument_list : argument
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_argument(p):
    """
    argument : pre_type_modifier type ID
    """

    pre_type = None
    if p[1] != "":
        pre_type = p[1]

    var_name = add_variable_declaration(p[3], p[2], pre_type)
    p[0] = (var_name, p[2], pre_type)


#Should only be called by the grammar. Call push_scope if needed instead
def p_push_scope(p):
    """
    push_scope :
    """
    p[0] = ""
    push_scope(p)


def push_scope(p):
    scope_stack.add_scope()


def pop_scope(p):
    scope_stack.pop_scope()


def add_variable_declaration(id, type, pre_type=None):
    scope = scope_stack.get_current_scope()

    global_var = False

    if not pre_type and scope_stack.scopes.index(scope) == 0:
        global_var = True

    return scope.add_declaration(id, type, pre_type, global_var)

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


def check_variable_in_current_scope(var):
    scope = scope_stack.get_current_scope()

    if scope.get_var(var):
        return True

    return False

def check_var_in_scope(var, p):
    if flags['ignore']:
        return 2

    if not scope_stack.get_var(p[1]):
        print_err("Variable \"" + p[1] + "\" hasn't been declared", p)
        #exit?
        return 0
    
    return 1


def get_initializer(type):
    initializer = "None"

    if type == "int":
        initializer = "0"
    elif type == "double":
        initializer = "0.0"
    elif type == "string":
        initializer = "\"\""
    elif type == "bool":
        initializer = "False"
    return initializer

def indent(p):
    if not p:
        return ""

    ret = []
    for s in p.split("\n"):
        ret.append("    " + s)
    return "\n".join(ret)


def in_function_parsing_phase():
    return flags['function_parsing']


def p_error(p):
    print_err("unknown text at " + p.value + ": line no " + str(p.lineno))


def print_err(error, p=None, force=False):
    if in_function_parsing_phase() and not force:
        return

    if p:
        error = error + ": " + str(p.lineno(1))

    print >>sys.stderr, error

    #raise Parse_Error(error)


parser = yacc.yacc()


if len(sys.argv) == 2:
    try:
        f = open(sys.argv[1])
        data = f.read()
        parser.parse(data)
        flags["function_parsing"] = False
        scope_stack = ScopeStack()

        #Had to call lex.lex() to restart line counting
        lex.lex()
        sys.stdout.write(parser.parse(data))

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
            parser.parse(expressions)






