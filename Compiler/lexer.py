import ply.lex as lex

class Lexer:

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

    def t_ID(self, t):
        r'[_a-zA-Z][_a-zA-Z0-9]*'
        t.type = Lexer.reserved.get(t.value, 'ID')
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    def t_COMMENT(self, t):
         r'/\*(/|(\*)*[^\*])*(\*)+/|//.*'
    #    return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def __init__(self):
        lex.lex(module=self)

    def lex(self):
        lex.lex(module=self)