from ply import yacc
from lexer import tokens, lexer
from maze import Maze, Bomb, Coin, Door, Key, Trap, Exit, Player, Warrior, Mage, Archer

current_maze = None
entry_position = None
exit_position = None
key_count = 0
door_count = 0

# Parsing rules
def p_program(p):
    'program : level'
    if key_count != door_count:
        raise ValueError(f"Number of keys ({key_count}) does not match number of doors ({door_count})")
    if not current_maze.add_entity(Player(current_maze), entry_position[0], entry_position[1]):
        raise ValueError(f"Error creating player at {entry_position}. Out of bounds, occupied, or not a path.")
    if not current_maze.add_entity(Exit(current_maze), exit_position[0], exit_position[1]):
        raise ValueError(f"Error creating exit at {exit_position}. Out of bounds, occupied, or not a path.")
    p[0] = current_maze

def p_level(p):
    'level : maze entry exit rooms paths obstacles'
    pass

def p_maze(p):
    'maze : MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA'
    global current_maze
    width, height = p[3]
    current_maze = Maze(width, height)

def p_dimensions(p):
    'dimensions : DIMENSIONS NUMBER X NUMBER'
    p[0] = (p[2], p[4])

def p_entry(p):
    'entry : ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global entry_position
    entry_position = (p[3], p[5])

def p_exit(p):
    'exit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global exit_position
    exit_position = (p[3], p[5])

def p_rooms(p):
    'rooms : ROOMS LLAVE_IZQ roomList LLAVE_DER'
    pass

def p_roomList(p):
    '''roomList : room roomList
                | '''
    pass

def p_room(p):
    'room : ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions PUNTO_COMA'
    x, y = p[4], p[6]
    width, height = p[8]
    if not current_maze.add_room(x, y, width, height):
        raise ValueError(f"Error creating room at ({x}, {y}) of {width} x {height}. Out of bounds or already exists.")

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
    if len(p) == 15:
        if not current_maze.add_path(p[4], p[6], p[10], p[12]):
            raise ValueError(f"Error creating path from ({p[4]}, {p[6]}) to ({p[10]}, {p[12]}). Out of bounds or already exists.")

def p_pointList(p):
    '''pointList : point pointList
                | '''
    pass

def p_point(p):
    'point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    if not current_maze.add_point(p[3], p[5]):
        raise ValueError(f"Error creating point ({p[3]}, {p[5]}). Out of bounds or already exists.")

def p_obstacles(p):
    'obstacles : OBSTACLES LLAVE_IZQ obstacleList LLAVE_DER'
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
    current_maze.add_entity(Bomb(current_maze), p[3], p[5])

def p_enemy(p):
    'enemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA'
    x, y = p[3], p[5]
    match p[8]:
        case "archer":
            if not current_maze.add_entity(Archer(current_maze), x, y):
                raise ValueError(f"Error creating archer at ({x}, {y}). Out of bounds, occupied or not a path.")
        case "warrior":
            if not current_maze.add_entity(Warrior(current_maze), x, y):
                raise ValueError(f"Error creating warrior at ({x}, {y}). Out of bounds, occupied or not a path.")
        case "mage":
            if not current_maze.add_entity(Mage(current_maze), x, y):
                raise ValueError(f"Error creating mage at ({x}, {y}). Out of bounds, occupied or not a path.")
        case _:
            raise ValueError(f"Invalid enemy type: {p[8]}")

def p_enemy_type(p):
    '''enemy_type : ARCHER
                  | WARRIOR
                  | MAGE'''
    p[0] = p[1].lower()

def p_door(p):
    'door : DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global door_count
    door_count += 1
    if not current_maze.add_entity(Door(current_maze), p[3], p[5]):
        raise ValueError(f"Error creating door at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")

def p_key(p):
    'key : KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global key_count
    key_count += 1
    if not current_maze.add_entity(Key(current_maze), p[3], p[5]):
        raise ValueError(f"Error creating key at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")

def p_coin(p):
    'coin : COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    if not current_maze.add_entity(Coin(current_maze), p[3], p[5]):
        raise ValueError(f"Error creating coin at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")

def p_trap(p):
    'trap : TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    if not current_maze.add_entity(Trap(current_maze, p[9], p[11]), p[3], p[5]):
        raise ValueError(f"Error creating trap at ({p[3]}, {p[5]}). Out of bounds, occupied, not a path or invalid target.")

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno}, column {p.lexpos})")
        print(f"Token: {p.type}, Value: {p.value}")
        print(f"Error occurred while parsing '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc(debug=True)

def parse(input_string):
    global current_maze
    current_maze = None  # Reset maze for each parse
    result = parser.parse(input_string, lexer=lexer)
    return result
