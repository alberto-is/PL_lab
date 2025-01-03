import ply.lex as lex

# Define reserved words as in the Keywords class
keywords = {
    'maze': 'MAZE',
    'dimensions': 'DIMENSIONS',
    'entry': 'ENTRY',
    'exit': 'EXIT',
    'rooms': 'ROOMS',
    'room': 'ROOM',
    'from': 'FROM',
    'to': 'TO',
    'paths': 'PATHS',
    'path': 'PATH',
    'point': 'POINT',
    'obstacles': 'OBSTACLES',
    'bomb': 'BOMB',
    'enemy': 'ENEMY',
    'door': 'DOOR',
    'key': 'KEY',
    'coin': 'COIN',
    'trap': 'TRAP',
    'type': 'TYPE',
    'archer': 'ARCHER',
    'warrior': 'WARRIOR',
    'mage': 'MAGE',
    'x': 'X'
}

# Tokens
tokens = [
    'NUMBER', 'ID',
    'LLAVE_IZQ', 'LLAVE_DER', 'PAREN_IZQ', 'PAREN_DER', 
    'PUNTO_COMA', 'COMA'
] + list(keywords.values())

# Regular expressions for the tokens
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_PUNTO_COMA = r';'
t_COMA = r','

# Handle reserved words
def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = keywords.get(t.value, 'ID')  # Check if it's a keyword
    return t

# Number rule
def t_NUMBER(t):
    r'[0-9]+'
    return t

# Ignoring whitespace
t_ignore = ' \t\r\n'

# Comments (single-line and multi-line)
def t_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*.*?\*/'
    pass

# Handle errors
def t_error(t):
    print(f"Error léxico: carácter no válido '{t.value[0]}'")
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()

# Test the lexer
def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
