import ply.yacc as yacc
from lexer import *
from helper import *

class Parser:

    def p_program(self, p):
        """
        program : statement_list
        """
        p[0] = p[1]


    def p_statement_list(self, p):
        """
        statement_list :
        statement_list : statement_list statement
        """
        if len(p) == 1:
            p[0] = ""
        else:
            p[0] = p[1] + ("\n" if p[1] else "") + p[2]


    def p_statement(self, p):
        """
        statement : function_declaration
        statement : compound_statement
        """
        p[0] = p[1]


    def p_compound_statement(self, p):
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


    def p_function_call_statement(self, p):
        """
        function_call_statement : ID LPAREN opt_parameter_list RPAREN
        """

        if in_function_parsing_phase():
            p[0] = ""
            return

        type = "unknown"
        text = None

        if p[1] not in functions:
            print_err("Call to undefined function '" + p[1] + "'", p)

        function = functions[p[1]]
        type = function.type

        function.check_parameters(p[3], p)

        param_list = [arg[0] for arg in p[3]]
        args_text = ", ".join(param_list)

        text = p[1] + "(" + args_text + ")"
        p[0] = Production(type=type, text=text, production_type="function_call", pre_type=function.pre_type)



    def p_opt_parameter_list(self, p):
        """
        opt_parameter_list : parameter_list
        opt_parameter_list :
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    def p_parameter_list(self, p):
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


    def p_variable_declaration(self, p):
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
                    var = get_var(p[1])
                    var_name = var["given_name"]

                    if var["global_var"] and flags["in_function"]:
                        pre_global_definition = "global " + var_name + "\n"

                    if var["type"] != p[3].type and var["type"] in numbers_list and p[3].type in numbers_list:
                        if var["type"] == "double":
                            assign_expr = "float(" + assign_expr + ")"
                        else:
                            assign_expr = "int(" + assign_expr + ")"

                    elif var["type"] != p[3].type and var["type"] in shapes_list:
                        if var["type"] != "Shape":
                            print_err("Invalid assignment: Trying to assign \"" + p[3].type + "\" to variable of type " + var["type"], p)
                    elif var["type"] != p[3].type:
                        print_err("Invalid assignment: Trying to assign \"" + p[3].type + "\" to variable of type " + var["type"], p)

                p[0] = pre_global_definition + var_name + " = " + assign_expr

        # Declaration and assignment
        elif len(p) == 6:
            var_name = add_variable_declaration(p[3], p[2], p[1])
            assign_expr = p[5].text

            pre_type = p[5].pre_type if p[5].pre_type else ""

            if p[2] != p[5].type and p[2] in numbers_list and p[5].type in numbers_list:
                if p[2] == "double":
                    assign_expr = "float(" + assign_expr + ")"
                else:
                    assign_expr = "int(" + assign_expr + ")"

            elif p[2] != p[5].type and p[2] in shapes_list:
                if p[2] != "Shape":
                    print_err("Invalid assignment: Trying to assign \"" + pre_type + " " + p[5].type + "\" to variable of type \"" + p[1] + " " +p[2] + "\"", p)

            elif p[2] != p[5].type:
                print_err("Invalid assignment: Trying to assign \"" + pre_type + " " + p[5].type + "\" to variable of type \"" + p[1] + " " +p[2] + "\"", p)


            if p[1] != pre_type:
                print_err("Invalid assignment: Trying to assign \"" + pre_type + " " + p[5].type + "\" to variable of type \"" + p[1] + " " +p[2] + "\"", p)


            p[0] = var_name + " = " + assign_expr


    def p_pre_type_modifier(self, p):
        """
        pre_type_modifier :
        pre_type_modifier : K_LIST
        """
        if len(p) == 1:
            p[0] = ""
        else:
            p[0] = p[1]

    def p_type(self, p):
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
        type : K_TABLE
        """
        p[0] = p[1]


    def p_expression(self, p):
        """
        expression : expression boolean_operator expression_pre_term
        expression : expression_pre_term
        """
        if in_function_parsing_phase():
            p[0] = ""
            return

        if len(p) == 4:
            expr = Production(pre_type=None)

            if p[1].pre_type == "list" or p[3].pre_type == "list":
                print_err("Expressions of type list are not compatible with \"" + p[2] + "\" operator", p)

            if p[1].type == "bool" and p[3].type == "bool":
                expr.type = "bool"
            else:
                print_err("\"" + p[2] + "\" symbol is not compatible with " + p[1].type + " " + p[3].type, p)

            expr.text = p[1].text + " " + p[2] + " " + p[3].text
            expr.children = [p[1], p[2], p[3]]
            p[0] = expr

        else:
            p[0] = p[1]


    def p_expression_pre_term(self, p):
        """
        expression_pre_term : expression_pre_term eq_comparator expression_term
        expression_pre_term : expression_term
        """
        if in_function_parsing_phase():
            p[0] = ""
            return

        if len(p) == 4:
            expr_term = Production(pre_type=None)

            if p[1].pre_type == "list" or p[3].pre_type == "list":
                print_err("Expressions of type list are not compatible with \"" + p[2] + "\" operator", p)

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

            if op == "=":
                op = "=="

            expr_term.text = p[1].text + " " + op + " " + p[3].text
            expr_term.children = [p[1], p[2], p[3]]

            p[0] = expr_term
        else:
            p[0] = p[1]


    def p_expression_term(self, p):
        """
        expression_term : expression_term comparator expression_factor
        expression_term : expression_factor
        """
        if in_function_parsing_phase():
            p[0] = ""
            return

        if len(p) == 4:
            expr_term = Production(pre_type=None)

            if p[1].pre_type == "list" or p[3].pre_type == "list":
                print_err("Expressions of type list are not compatible with \"" + p[2] + "\" operator", p)

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


    def p_expression_factor(self, p):
        """
        expression_factor : expression_factor op unary_expression
        expression_factor : unary_expression
        """
        if in_function_parsing_phase():
            p[0] = ""
            return

        if len(p) == 4:
            expr_factor = Production(pre_type=None)

            if p[1].pre_type == "list" or p[3].pre_type == "list":
                print_err("Expressions of type list are not compatible with \"" + p[2] + "\" operator", p)

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


    def p_op(self, p):
        """
        op : PLUS
        op : MINUS
        op : TIMES
        op : DIVIDE
        op : MOD
        """
        p[0] = p[1]


    def p_boolean_operator(self, p):
        """
        boolean_operator : AND
        boolean_operator : OR
        """
        if p[1] == "&&":
            p[0] = "and"
        else:
            p[0] = "or"


    def p_primary_expression(self, p):
        """
        primary_expression : constant
        primary_expression : id_expression
        primary_expression : function_call_statement
        primary_expression : MINUS primary_expression
        primary_expression : null_expression
        """
        #@todo type checking
        if len(p) == 3:
            if p[2].type in numbers_list:
                if p[2].pre_type == "list":
                    print_err("Expressions of type list are not compatible with - operator", p)

                p[2].text = "-" + p[2].text
                p[0] = p[2]
            else:
                print_err("Unary \"-\" can only be used to denote negative integers", p)
                p[0] = p[2]
        else:
            p[0] = p[1]


    def p_id_expression(self, p):
        """
        id_expression : ID
        """

        prod = Production(text=p[1],children=[p[1]], production_type="id")

        check_result = check_var_in_scope(p[1], p)

        if check_result == 1:
            var = get_var(p[1])

            prod.text = var['given_name']

            prod.type = var["type"]
            prod.pre_type = var["pre_type"]
        elif check_result == 2: #Variable is assigned as return value of function. Ignoreflag is true
            pass
        else:
            print_err("Variable \"" + p[1] + "\" used before declared", p)

        p[0] = prod


    def p_constant(self, p):
        """
        constant : boolean_constant
        constant : number
        constant : string_constant
        """
        p[1].production_type = "constant"
        p[0] = p[1]


    def p_string_constant(self, p):
        """
        string_constant : STRING
        """
        p[0] = Production(type="string", text=p[1], children=[p[1]])


    def p_boolean_constant(self, p):
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


    def p_unary_expression(self, p):
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
                if p[2].pre_type == "list":
                    print_err("Expressions of type list are not compatible with \"!\" operator", p)

                p[2].text = " not " + p[2].text
                p[0] = p[2]
            else:
                print_err("\"!\" operator can only be used with boolean expressions", p)
        elif len(p) == 5:
            if p[3].type == "bool":
                if p[3].pre_type == "list":
                    print_err("Expressions of type list are not compatible with \"!\" operator", p)

                p[3].text = " not (" + p[3].text + ")"
                p[0] = p[3]
            else:
                print_err("\"!\" operator can only be used with boolean expressions", p)
        else:
            p[0] = p[1]

    def p_null_expression(self, p):
        """
        null_expression : K_NULL
        """
        p[0] = Production(type="Shape", text="None", children=[p[1]])

    def p_comparator(self, p):
        """
        comparator : GT
        comparator : LT
        comparator : GEQ
        comparator : LEQ
        """
        p[0] = p[1]


    def p_eq_comparator(self, p):
        """
        eq_comparator : EQ
        eq_comparator : NEQ
        """
        p[0] = p[1]

    def p_number(self, p):
        """
        number : integer_number
        number : double_number
        """
        p[0] = p[1]


    def p_integer_number(self, p):
        """
        integer_number : INTEGER
        """
        p[0] = Production(type="int", text=p[1], children=[p[1]])


    def p_double_number(self, p):
        """
        double_number : DOUBLE
        """
        p[0] = Production(type="double", text=p[1], children=[p[1]])

    def p_selection_statement(self, p):
        """
        selection_statement :   if_statement \
                                else_if_statement_list \
                                else_statement \
                            K_END
        """
        p[0] = p[1] + ("\n" if p[2] else "") + p[2] + ("\n" if p[3] else "") + p[3]


    def p_if_statement(self, p):
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


    def p_else_if_statement_list(self, p):
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


    def p_else_if_statement(self, p):
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


    def p_else_statement(self, p):
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


    def p_compound_statement_list(self, p):
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


    def p_iteration_statement(self, p):
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


    def p_iteration_statement_header(self, p):
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


    def p_jump_statement(self, p):
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
                print_err("\"" + p[1] + "\"" + " can only be used inside a function", p, False, True)

        elif p[1] == "break":
            if flags["in_while"] > 0:
                p[0] = "break"
            else:
                p[0] = ""
                print_err("\"" + p[1] + "\"" + " can only be used inside a while loop", p, False, True)
        else:
            if flags["in_while"] > 0:
                p[0] = "continue"
            else:
                p[0] = ""
                print_err("\"" + p[1] + "\"" + " can only be used inside a while loop", p, False, True)


    def p_function_declaration(self, p):
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


    def p_function_header(self, p):
        """
        function_header : pre_type_modifier type ID LPAREN push_scope opt_argument_list RPAREN ASSIGN set_ignore_flag \
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

        init_ret = None

        arg_list = [arg[0] for arg in p[6]]
        args_text = ", ".join(arg_list)

        #if not an ID
        ret_expression = p[10].text
        if p[10].production_type == 'id':
            if not check_variable_in_current_scope(p[10].text):
                var_name = add_variable_declaration(p[10].text, p[2], p[1])

                initializer = get_initializer(p[2], p[1])

                init_ret = var_name + " = " + initializer
                ret_expression = var_name

            # check to make sure the argument has the same type
            else:
                var = get_var(p[10].text)
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

        flags["in_function"] = True
        flags["return_expression"] = ret_expression

        p[0] = (text, ret_expression)

        if in_function_parsing_phase():
            functions[p[3]] = f


    def p_opt_argument_list(self, p):
        """
        opt_argument_list : argument_list
        opt_argument_list :
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    def p_argument_list(self, p):
        """
        argument_list : argument_list COMMA argument
        argument_list : argument
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]


    def p_argument(self, p):
        """
        argument : pre_type_modifier type ID
        """

        pre_type = None
        if p[1] != "":
            pre_type = p[1]

        var_name = add_variable_declaration(p[3], p[2], pre_type)
        p[0] = (var_name, p[2], pre_type)


    #Should only be called by the grammar. Call push_scope if needed instead
    def p_push_scope(self, p):
        """
        push_scope :
        """
        p[0] = ""
        push_scope(p)

    def p_set_ignore_flag(self, p):
        """
        set_ignore_flag :
        """
        flags['ignore'] = True

        p[0] = ""

    def p_unset_ignore_flag(self, p):
        """
        unset_ignore_flag :
        """
        flags['ignore'] = False
        p[0] = ""

    def p_error(self, p):
        print_err("unknown text at " + p.value + ": line no " + str(p.lineno))

    def __init__(self):
        self.lexer = lexer = Lexer()
        self.tokens = tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self)
