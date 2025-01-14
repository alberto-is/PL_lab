from ply import yacc
from lexer import tokens, lexer
from maze import Maze, Bomb, Coin, Door, Key, Trap, Exit, Player, Warrior, Mage, Archer

current_maze = None  # Maze object
key_count = 0
door_count = 0
create_maze = True  # Flag to check if a maze can be created

def p_program(p):
    'program : level'
    global create_maze
    if key_count < door_count:
        print(f"ERROR: Number of keys ({key_count}) is not equal or larger than number of doors ({door_count})")
        create_maze = False
    p[0] = current_maze

def p_level(p):
    'level : maze entry exit rooms paths obstacles'
    global create_maze
    entry_pos = p[2]
    exit_pos = p[3]
    if not current_maze.add_entity(Player(current_maze), entry_pos[0], entry_pos[1]):
        print(f"ERROR: Cannot create player at {entry_pos}. Out of bounds, occupied, or not a path.")
        create_maze = False
    if not current_maze.add_entity(Exit(current_maze), exit_pos[0], exit_pos[1]):
        print(f"ERROR: Cannot create exit at {exit_pos}. Out of bounds, occupied, or not a path.")
        create_maze = False

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
    p[0] = (p[3], p[5])

def p_exit(p):
    'exit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    p[0] = (p[3], p[5])

def p_rooms(p):
    'rooms : ROOMS LLAVE_IZQ roomList LLAVE_DER'
    pass

def p_roomList(p):
    '''roomList : room roomList
                | '''
    pass

def p_room(p):
    'room : ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions PUNTO_COMA'
    global create_maze
    x, y = p[4], p[6]
    width, height = p[8]
    if not current_maze.add_room(x, y, width, height):
        print(f"ERROR: Cannot create room at ({x}, {y}) of {width} x {height}. Out of bounds or already exists.")
        create_maze = False

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
    global current_maze
    if len(p) == 15:
        if not current_maze.add_path(p[4], p[6], p[10], p[12]):
            print(f"ERROR: Cannot create path from ({p[4]}, {p[6]}) to ({p[10]}, {p[12]}). Out of bounds or already exists.")
            create_maze = False

def p_pointList(p):
    '''pointList : point pointList
                | '''
    pass

def p_point(p):
    'point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    if not current_maze.add_point(p[3], p[5]):
        print(f"ERROR: Cannot create point ({p[3]}, {p[5]}). Out of bounds or already exists.")
        create_maze = False

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
    global create_maze
    if not current_maze.add_entity(Bomb(current_maze), p[3], p[5]):
        print(f"ERROR: Cannot create bomb at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")
        create_maze = False

def p_enemy(p):
    'enemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA'
    global create_maze
    x, y = p[3], p[5]
    match p[8]:
        case "archer":
            if not current_maze.add_entity(Archer(current_maze), x, y):
                print(f"ERROR: Cannot create archer at ({x}, {y}). Out of bounds, occupied or not a path.")
                create_maze = False
        case "warrior":
            if not current_maze.add_entity(Warrior(current_maze), x, y):
                print(f"ERROR: Cannot create warrior at ({x}, {y}). Out of bounds, occupied or not a path.")
                create_maze = False
        case "mage":
            if not current_maze.add_entity(Mage(current_maze), x, y):
                print(f"ERROR: Cannot create mage at ({x}, {y}). Out of bounds, occupied or not a path.")
                create_maze = False
        case _:
            print(f"ERROR: Invalid enemy type '{p[8]}'. Must be 'archer', 'warrior' or 'mage'.")
            create_maze = False

def p_enemy_type(p):
    '''enemy_type : ARCHER
                  | WARRIOR
                  | MAGE'''
    p[0] = p[1].lower()

def p_door(p):
    'door : DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global door_count, create_maze
    door_count += 1
    if not current_maze.add_entity(Door(current_maze), p[3], p[5]):
        print(f"ERROR: Cannot create door at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")
        create_maze = False

def p_key(p):
    'key : KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global key_count, create_maze
    key_count += 1
    if not current_maze.add_entity(Key(current_maze), p[3], p[5]):
        print(f"ERROR: Cannot create key at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")
        create_maze = False

def p_coin(p):
    'coin : COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global create_maze
    if not current_maze.add_entity(Coin(current_maze), p[3], p[5]):
        print(f"ERROR: Cannot create coin at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")
        create_maze = False

def p_trap(p):
    'trap : TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global create_maze
    if not current_maze.add_entity(Trap(current_maze, p[9], p[11]), p[3], p[5]):
        print(f"ERROR: Cannot create trap at ({p[3]}, {p[5]}). Out of bounds, occupied or not a path.")
        create_maze = False

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
    global current_maze, create_maze
    current_maze = None  # Reset maze for each parse
    result = parser.parse(input_string, lexer=lexer)
    if not create_maze:
        result = None
    return result
