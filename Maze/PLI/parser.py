import ply.yacc as yacc
from lexer import lexer
from lexer import tokens

# Precedence and associativity (if any) could be defined here
# precedence = ()

# Parsing rules
def p_program(p):
    'program : level'
    pass

def p_level(p):
    'level : maze entry exit rooms paths obstacles'
    pass

def p_maze(p):
    'maze : MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA'
    pass

def p_dimensions(p):
    'dimensions : DIMENSIONS NUMBER X NUMBER'
    pass

def p_entry(p):
    'entry : ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_exit(p):
    'exit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_rooms(p):
    'rooms : ROOMS LLAVE_IZQ roomList LLAVE_DER'
    pass

def p_roomList(p):
    '''roomList : room roomList
                | '''
    pass

def p_room(p):
    'room : ROOM ID FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions LLAVE_IZQ obstacleList LLAVE_DER'
    pass

def p_obstacleList(p):
    '''obstacleList : obstacle obstacleList
                    | '''
    pass

def p_obstacle(p):
    '''obstacle : bomb
                | enemy
                | door
                | key
                | coin
                | trap'''
    pass

def p_bomb(p):
    'bomb : BOMB PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_enemy(p):
    'enemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA'
    pass

def p_enemy_type(p):
    '''enemy_type : ARCHER
                  | WARRIOR
                  | MAGE'''
    pass

def p_door(p):
    'door : DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_key(p):
    'key : KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_coin(p):
    'coin : COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_trap(p):
    'trap : TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_paths(p):
    'paths : PATHS LLAVE_IZQ pathList LLAVE_DER'
    pass

def p_pathList(p):
    '''pathList : path pathList
                | '''
    pass

def p_path(p):
    '''path : PATH FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA
           | PATH LLAVE_IZQ pointList LLAVE_DER'''
    pass

def p_pointList(p):
    '''pointList : point pointList
                | '''
    pass

def p_point(p):
    'point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    pass

def p_obstacles(p):
    'obstacles : OBSTACLES LLAVE_IZQ obstacleList LLAVE_DER'
    pass

def p_number(p):
    'number : NUMBER'
    pass

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(debug=True)

def parse(input_string):
    return parser.parse(input_string, lexer=lexer)