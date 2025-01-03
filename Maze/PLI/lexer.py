from ply import lex

# Lista de nombres de tokens - es importante que coincidan exactamente con los usados en el parser
tokens = [
    'NUMBER',
    'ID',
    'PAREN_IZQ',
    'PAREN_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'PUNTO_COMA',
    'COMA',
] + [
    'MAZE',
    'DIMENSIONS',
    'ENTRY',
    'EXIT',
    'ROOMS',
    'ROOM',
    'FROM',
    'TO',
    'PATHS',
    'PATH',
    'POINT',
    'OBSTACLES',
    'BOMB',
    'ENEMY',
    'TYPE',
    'DOOR',
    'KEY',
    'COIN',
    'TRAP',
    'ARCHER',
    'WARRIOR',
    'MAGE',
    'X'
]

# Diccionario de palabras reservadas
reserved = {
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
    'type': 'TYPE',
    'door': 'DOOR',
    'key': 'KEY',
    'coin': 'COIN',
    'trap': 'TRAP',
    'archer': 'ARCHER',
    'warrior': 'WARRIOR',
    'mage': 'MAGE',
    'x': 'X'
}

# Reglas simples para tokens
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_PUNTO_COMA = r';'
t_COMA = r','

# Regla para ignorar espacios y tabulaciones
t_ignore = ' \t\r'

# Regla para nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Regla para números
def t_NUMBER(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    return t

# Reglas para comentarios
def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

# Regla para errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
