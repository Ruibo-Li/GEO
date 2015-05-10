import sys

numbers_list = [
    "int",
    "double"
]

shapes_list = [
    "Shape",
    "Rectangle",
    "Circle",
    "Triangle",
    "Point",
    "Line",
    "Text",
    "Table"
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

    def add_declaration(self, id, type, pre_type=None, global_var=False, p=None):
        if id in self.vars:
            print_err("Variable '" + id + "' was already declared", p)

        pre_type = pre_type if pre_type and pre_type != '' else None

        self.vars[id] = {
            'type': type,
            'pre_type': pre_type,
            'given_name': id + '_' + str(len(scope_stack.scopes)),
            'global_var': global_var
        }

        return self.vars[id]['given_name']

    def get_var(self, id):
        if id in self.vars:
            return self.vars[id]
        return None


class Function:
    def __init__(self, type=None, name=None, args=[], pre_type=None, match=None):
        self.type = type
        self.args = args
        self.name = name
        self.pre_type = pre_type
        self.match = match

    def get_type(self, params):
        if self.type == "any":
            return params[self.match][1]
        return self.type

    def check_parameters(self, param_list, p=None):
        args = self.args
        
        if len(param_list) != len(args):
            print_err("Function " + self.name + " expects " + str(len(args)) + " arguments. " + str(len(param_list)) + " received", p)
            return False

        for i in xrange(len(param_list)):
            param = param_list[i]
            param_type = param[1]
            param_pre_type = param[2]
            arg = args[i]
            arg_type = arg["type"]
            arg_pre_type = arg["pre_type"]

            param_pre_type_text = param_pre_type if param_pre_type else ""
            arg_pre_type_text = arg_pre_type if arg_pre_type else ""

            if param_pre_type != arg_pre_type:
                print_err("Function " + self.name + " expects argument of type '" + arg_pre_type_text + " " + arg_type + "' at position " + str(i + 1) + ". " + param_pre_type_text + " " + param_type + " received instead" , p)

            if arg_type == "any":
                if "match" in arg:
                    for m in arg["match"]:
                        if param_type != param_list[m][1]:
                            param_pre_type_text = param_list[m][2] if param_list[m][2] else ""
                            print_err("Function " + self.name + " expects argument of type " + param_type + " at position " + str(m) + ". " + param_pre_type_text + " " + param_list[m][1] + " received instead", p)
                            return False
            elif arg_type == "Shape":
                if param_type not in shapes_list:
                    print_err("Function " + self.name + " expects argument of type '" + arg_pre_type_text + " " + arg_type + "' at position " + str(i + 1) + ". " + param_pre_type_text + " " + param_type + " received instead" , p)
                    return False
            elif arg_type == "number":
                if param_type not in numbers_list:
                    print_err("Function " + self.name + " expects argument of type '" + arg_pre_type_text + " " + arg_type + "' at position " + str(i + 1) + ". " + param_pre_type_text + " " + param_type + " received instead" , p)
                    return False
            elif arg_type != param_type:
                print_err("Function " + self.name + " expects argument of type '" + arg_pre_type_text + " " + arg_type + "' at position " + str(i + 1) + ". " + param_pre_type_text + " " + param_type + " received instead" , p)
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

functions = {
    "randomNum" : Function(
        name="randomNum",
        type="double",
        args=[]
    ),
    "randomInt" : Function(
        name="randomInt",
        type="int",
        args=[
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),

    # List functions
    "listAppend" : Function(
        name="listAppend",
        type="null",
        args=[
                {"type": "any", "pre_type": "list", "match": [1]},
                {"type": "any", "pre_type": None}
        ]
    ),
    "listExtend" : Function(
        name="listExtend",
        type="unassignable",
        pre_type="list",
        args=[
                {"type": "any", "pre_type": "list", "match": [1]},
                {"type": "any", "pre_type": "list"}
        ]
    ),
    "listInsert" : Function(
        name="listInsert",
        type="unassignable",
        args=[
                {"type": "any", "pre_type": "list", "match": [2]},
                {"type": "int", "pre_type": None},
                {"type": "any", "pre_type": None}
        ]
    ),
    "listRemove" : Function(
        name="listRemove",
        type="unassignable",
        args=[
                {"type": "any", "pre_type": "list"},
                {"type": "int", "pre_type": None}
        ]
    ),
    "listIndex" : Function(
        name="listIndex",
        type="int",
        args=[
                {"type": "any", "pre_type": "list", "match":[1]},
                {"type": "any", "pre_type": None}
        ]
    ),
    "listCount" : Function(
        name="listCount",
        type="int",
        args=[
                {"type": "any", "pre_type": "list", "match":[1]},
                {"type": "any", "pre_type": None}
        ]
    ),
    "listSort" : Function(
        name="listSort",
        type="unassignable",
        args=[
                {"type": "any", "pre_type": "list"}
        ]
    ),
    "listReverse" : Function(
        name="listReverse",
        type="unassignable",
        args=[
                {"type": "any", "pre_type": "list"}
        ]
    ),
    "listGet" : Function(
        name="listGet",
        type="any",
        match=1,
        args=[
                {"type": "any", "pre_type": "list"},
                {"type": "int", "pre_type": None}
        ]
    ),
    "listPop" : Function(
        name="listPop",
        type="any",
        match=0,
        args=[
                {"type": "any", "pre_type": "list"}
        ]
    ),
    "listSet" : Function(
        name="listSet",
        type="unassignable",
        args=[
                {"type": "any", "pre_type": "list", "match": [2]},
                {"type": "int", "pre_type": None},
                {"type": "any", "pre_type": None}
        ]
    ),

    #String functions
    "str" : Function(
        name="str",
        type="string",
        args=[
                {"type": "number", "pre_type": None}
        ]
    ),
    "print" : Function(
        name="print",
        type="unsassignable",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "printf" : Function(
        name="printf",
        type="unsassignable",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "printl" : Function(
        name="printl",
        type="unsassignable",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "split" : Function(
        name="split",
        type="string",
        pre_type="list",
        args=[
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "strip" : Function(
        name="strip",
        type="string",
        args=[
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "replaceString" : Function(
        name="strip",
        type="string",
        args=[
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "findSubstring" : Function(
        name="findSubstring",
        type="int",
        args=[
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "isDigit" : Function(
        name="isDigit",
        type="bool",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "isUpper" : Function(
        name="isUpper",
        type="bool",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "isLower" : Function(
        name="isLower",
        type="bool",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "lower" : Function(
        name="lower",
        type="string",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "upper" : Function(
        name="upper",
        type="string",
        args=[
                {"type" : "string", "pre_type": None}
        ]
    ),
    "joinString" : Function(
        name="joinString",
        type="string",
        args=[
                {"type" : "string", "pre_type": None},
                {"type" : "string", "pre_type": "list"}
        ]
    ),

    #Color functions
    "RGB2Str" : Function(
        name="RGB2Str",
        type="string",
        args=[
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "getR" : Function(
        name="getR",
        type="int",
        args=[
                {"type": "string", "pre_type": None}
        ]
    ),
    "getG" : Function(
        name="getG",
        type="int",
        args=[
                {"type": "string", "pre_type": None}
        ]
    ),
    "getB" : Function(
        name="getB",
        type="int",
        args=[
                {"type": "string", "pre_type": None}
        ]
    ),

    #Shape functions
    "createWindow" : Function(
        name="listAppend",
        type="Window",
        args=[
                {"type": "string", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
            ]
    ),
    "createTriangle" : Function(
        name="createTriangle",
        type="Triangle",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Point", "pre_type": None},
                {"type": "Point", "pre_type": None}
        ]
    ),
    "createRectangle" : Function(
        name="createRectangle",
        type="Rectangle",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Point", "pre_type": None}
        ]
    ),
    "createCircle" : Function(
        name="createCircle",
        type="Circle",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "createPoint" : Function(
        name="createPoint",
        type="Point",
        args=[
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "createLine" : Function(
        name="createLine",
        type="Line",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Point", "pre_type": None}
        ]
    ),
    "createTable" : Function(
        name="createTable",
        type="Table",
        args=[
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "createText" : Function(
        name="createText",
        type="Text",
        args=[
                {"type": "Point", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "render" : Function(
        name="render",
        type="unsassignable",
        args=[
                {"type": "Window", "pre_type": None},
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "remove" : Function(
        name="remove",
        type="unassignable",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "move" : Function(
        name="move",
        type="unsassignable",
        args=[
                {"type": "Shape", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "areSimilar" : Function(
        name="areSimilar",
        type="bool",
        args=[
                {"type" : "Triangle", "pre_type" : None},
                {"type" : "Triangle", "pre_type" : None}
        ]
    ),
    "getDistance" : Function(
        name="getDistance",
        type="double",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Point", "pre_type": None}
        ]
    ),
    "isVertical" : Function(
        name="isVertical",
        type="bool",
        args=[
                {"type": "Line", "pre_type": None}
        ]
    ),
    "cross" : Function(
        name="cross",
        type="bool",
        args=[
                {"type": "Line", "pre_type": None},
                {"type": "Line", "pre_type": None}
        ]
    ),
    "pointToLine" : Function(
        name="pointToLine",
        type="double",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Line", "pre_type": None}
        ]
    ),
    "intersect" : Function(
        name="intersect",
        type="bool",
        args=[
                {"type": "Shape", "pre_type": None},
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "inside" : Function(
        name="inside",
        type="bool",
        args=[
                {"type": "Point", "pre_type": None},
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToTriangle" : Function(
        name="shapeToTriangle",
        type="Triangle",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToRectangle" : Function(
        name="shapeToRectangle",
        type="Rectangle",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToCircle" : Function(
        name="shapeToCircle",
        type="Circle",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToLine" : Function(
        name="shapeToLine",
        type="Line",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToPoint" : Function(
        name="shapeToPoint",
        type="Point",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "shapeToTable" : Function(
        name="shapeToTable",
        type="Table",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "setColor" : Function(
        name="setColor",
        type="unassignable",
        args=[
                {"type": "Shape", "pre_type": None},
                {"type": "string", "pre_type": None}
        ]
    ),
    "getColor" : Function(
        name="getColor",
        type="string",
        args=[
                {"type": "Shape", "pre_type": None}
        ]
    ),
    "setCellColor" : Function(
        name="setCellColor",
        type="unassignable",
        args=[
                {"type": "Table", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "string", "pre_type": None}
        ]
    ),
    "getCell" : Function(
        name="getCell",
        type="Rectangle",
        args=[
                {"type": "Table", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "getACell" : Function(
        name="getACell",
        type="Rectangle",
        args=[
            {"type": "Table", "pre_type": None},
            {"type": "int", "pre_type": None},
            {"type": "int", "pre_type": None}
        ]
    ),
    "getRow" : Function(
        name="getRow",
        type="int",
        args=[
                {"type": "Table", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "getCol" : Function(
        name="getCol",
        type="int",
        args=[
                {"type": "Table", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "getX" : Function(
        name="getX",
        type="int",
        args=[
                {"type": "Point", "pre_type": None}
        ]
    ),
    "getY" : Function(
        name="getY",
        type="int",
        args=[
                {"type": "Point", "pre_type": None}
        ]
    ),
    "getVal" : Function(
        name="getVal",
        type="int",
        args=[
                {"type": "Table", "pre_type": None},
                {"type": "int", "pre_type": None},
                {"type": "int", "pre_type": None}
        ]
    ),
    "getMouse" : Function(
        name="getMouse",
        type="Point",
        args=[
                {"type": "Window", "pre_type": None}
        ]
    ),
    "hasSameColor" : Function(
        name="hasSameColor",
        type="bool",
        args=[
                {"type": "Table", "pre_type": None},
                {"type" : "string", "pre_type": None}
        ]
    ),
    "shapeHaveSameColor" : Function(
        name="shapeHaveSameColor",
        type="bool",
        args=[
                {"type": "Shape", "pre_type": None},
                {"type": "Shape", "pre_type": None}
        ]
    )
}

scope_stack = None


def init_scope_stack():
    global scope_stack
    scope_stack = ScopeStack()

init_scope_stack()

# Flag set to true to ignore variable declaration checking
flags = {
    "ignore": False,
    "function_parsing": True,
    "in_function": False,
    "in_while": 0,  # nested whiles
    "return_expression": None
}


def push_scope(p):
    scope_stack.add_scope()


def pop_scope(p):
    scope_stack.pop_scope()


def add_variable_declaration(id, type, pre_type=None, p=None):
    scope = scope_stack.get_current_scope()

    global_var = False

    if not pre_type and scope_stack.scopes.index(scope) == 0:
        global_var = True

    return scope.add_declaration(id, type, pre_type, global_var, p)


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
        # exit?
        return 0

    return 1


def get_var(var):
    return scope_stack.get_var(var)


def get_initializer(type, pre_type=None):
    if pre_type == "list":
        return "[]"

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


def print_err(error, p=None, force=False, ignore=False):
    if in_function_parsing_phase() and not force:
        return

    if p:
        lineError = ": " + str(p.lineno(1)) if p.lineno(1) != 0 else ""
        error = error + lineError

    print >>sys.stderr, error

    if not ignore:
        raise Parse_Error(error)
