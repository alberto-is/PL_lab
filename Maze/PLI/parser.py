import ply.yacc as yacc
from ply.lex import LexToken

# First, we'll use the lexer from above
# Define the token list and reserved words again to be used in parsing

# Define the token names, precedence, and grammar
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

# Define the grammar (using PLY format)
def p_level(p):
    'level : maze entry exit rooms paths obstacles'
    print(f"Level parsed: {p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}")

def p_maze(p):
    'maze : MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA'
    print(f"Maze parsed with dimensions: {p[3]}")

def p_dimensions(p):
    'dimensions : DIMENSIONS NUMBER X NUMBER'
    p[0] = (p[2], p[4])
    print(f"Dimensions: {p[0]}")

def p_entry(p):
    'entry : ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    print(f"Entry: {p[3]}, {p[5]}")

def p_exit(p):
    'exit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    print(f"Exit: {p[3]}, {p[5]}")

def p_rooms(p):
    'rooms : ROOMS LLAVE_IZQ room_list LLAVE_DER'
    print(f"Rooms: {p[3]}")

def p_room_list(p):
    '''room_list : room room_list
                 | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_room(p):
    'room : ROOM ID FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions LLAVE_IZQ obstacle_list LLAVE_DER'
    print(f"Room: {p[2]}, Location: {p[5]}, {p[7]}")

def p_obstacle_list(p):
    '''obstacle_list : obstacle obstacle_list
                     | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Define other rules for obstacles, bombs, enemies, etc.
def p_obstacle(p):
    '''obstacle : bomb
                | enemy
                | door
                | key
                | coin
                | trap'''
    p[0] = p[1]

def p_bomb(p):
    'bomb : BOMB PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    print(f"Bomb at: {p[3]}, {p[5]}")

def p_enemy(p):
    'enemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA'
    print(f"Enemy at: {p[3]}, {p[5]}, Type: {p[7]}")

def p_enemy_type(p):
    '''enemy_type : ARCHER
                  | WARRIOR
                  | MAGE'''
    p[0] = p[1]

# Define precedence for operators if needed
precedence = (
    ('left', 'PUNTO_COMA'),
)

# Error handling
def p_error(p):
    print(f"Syntax error at {p.value}" if p else "Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test parsing function
def test_parser(data):
    parser.parse(data)

