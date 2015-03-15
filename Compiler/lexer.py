import ply.lex as lex


reserved = {
    'if' : 'K_IF',
    'ef' : 'K_EF',
    'el' : 'K_EL',
    'end' : 'K_END',
    'while' : 'K_WHILE',
    'int' : 'K_INT',
    'double' : 'K_DOUBLE',
    'null' : 'K_NULL',
    'list' : 'K_LIST',
    'Window' : 'K_WINDOW',
    'Triangle' : 'K_TRIANGLE',
    'Circle' : 'K_CIRCLE',
    'Shape' : 'K_SHAPE',
    'Rectangle' : 'K_RECTANGLE',
    'Point' : 'K_POINT',
    'bool' : 'K_BOOL',
    'true' : 'K_TRUE',
    'false' : 'K_FALSE'
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
  r'/\*(/|(\*)*[^\*])*(\*)+/|//.*\n'
  return t  

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
/* This demo2 function renders a random figure of random size upon 
   receiving a mouse click and returns the current board. */

// Define function demo2() that returns a board
Window demo2() := board
    // Init and set board size in pixels
    board := Window(500, 500)
    while (true)
        int i := random(1, 4)
        int x := random(0, 600)
        int y := random(0, 100)
        int width := random(100, 300)
        int length := random(100, 300)
        Shape shape := null

        if (i = 1)
            shape := Rectangle(Point(x, y), Point(x + width, y + length))
        ef (i = 2)
            shape := Circle(Point(x, y), length)
        el
            shape := Triangle(Point(x, y), Point(x + width, y + length), 
                Point(x, y + length))
        end

        // Render the random figure and pause for user input
        render(board, shape)
        list coords := getMouse()
        // Prompt user input until a valid mouse click
        while (!in(shape, coords))
            coords := getMouse()
        end
        remove(board, shape)

    end
end


'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
