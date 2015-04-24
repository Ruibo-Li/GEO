import sys

numbers_list = [
    "int",
    "double"
]

shapes_list = [
    "Shape",
    "Rectangle",
    "Circle",
    "Triangle"
]

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
    def __init__(self, type=None, name=None, args=[], pre_type=None):
        self.type = type
        self.args = args
        self.name = name
        self.pre_type = pre_type

    def check_parameters(self, param_list, p=None):
        args = self.args
        
        if len(param_list) != len(args):
            print_err("Function " + self.name + " expects " + str(len(args)) + " arguments. " + str(len(param_list)) + " received", p)
            return False

        for i in xrange(len(param_list)):
            param_type = param_list[i][1]
            arg_type = args[i]["type"]

            if arg_type == "Shape":
                if param_type not in shapes_list:
                    print_err("Function " + self.name + " expects argument of type '" + arg_type + "' at position " + str(i + 1) + ". " + param_type +" received instead" , p)
                    return False
            elif arg_type == "number":
                if param_type not in numbers_list:
                    print_err("Function " + self.name + " expects argument of type '" + arg_type + "' at position " + str(i + 1) + ". " + param_type +" received instead" , p)
                    return False
            elif args[i]['type'] != param_list[i][1]:
                print_err("Function " + self.name + " expects argument of type '" + arg_type + "' at position " + str(i + 1) + ". " + param_type +" received instead" , p)
                return False
        return True

    def __str__(self):
        return "(type=" + self.type +", args=" + str(self.args) + ", name=" + self.name + ", pre_type=" + self.pre_type + ")"

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
    "str" : Function(type="string", args=[{"type": "number", "pre_type": None}], name="str"),
    "render": Function(type="null", args=[{"type": "Shape", "pre_type": None}], name="render")
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

def print_err(error, p=None, force=False):
    if in_function_parsing_phase() and not force:
        return

    if p:
        error = error + ": " + str(p.lineno(1))

    print >>sys.stderr, error
    raise Parse_Error(error)
