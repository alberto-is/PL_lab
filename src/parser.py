from ply import yacc
from lexer import tokens, lexer 
from maze import Maze, Bomb, Coin, Door, Key, Trap, Exit, Player, Warrior, Mage, Archer

current_maze = None
door_count = 0
key_count = 0
entry_position = None
exit_position = None

def p_program(p):
    'program : level'
    p[0] = current_maze if current_maze else None

def p_level(p):
    'level : maze entry exit rooms paths obstacles'
    # Add player and exit after the maze and paths are fully defined
    if entry_position:
        x, y = entry_position
        cell = current_maze.matrix[y][x]
        if not cell.is_path:
            raise Exception(f"Invalid player entry position: {entry_position} - Not a path.")
        if not current_maze.add_entity(Player(current_maze), x, y):
            raise Exception(f"Failed to add player at {entry_position}")
    
    if exit_position:
        x, y = exit_position
        cell = current_maze.matrix[y][x]
        if not cell.is_path:
            raise Exception(f"Invalid exit position: {exit_position} - Not a path.")
        if not current_maze.add_entity(Exit(current_maze), x, y):
            raise Exception(f"Failed to add exit at {exit_position}")

def p_maze(p):
    'maze : MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA'
    global current_maze
    width, height = p[3]
    current_maze = Maze(width, height)  # Initialize maze with the correct dimensions

def p_dimensions(p):
    'dimensions : DIMENSIONS NUMBER X NUMBER'
    p[0] = (p[2], p[4])  # width, height

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
    'room : ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions LLAVE_DER'
    if not current_maze.add_room(p[4], p[6], p[8][0], p[8][1]):
        raise Exception(f"Invalid room starting at ({p[4]}, {p[6]}) with dimensions {p[8]}")

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
    if not current_maze.add_entity(Bomb(current_maze), p[3], p[5]):
        raise Exception(f"Invalid bomb position: ({p[3]}, {p[5]})")

def p_door(p):
    'door : DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global door_count
    door_count += 1
    if not current_maze.add_entity(Door(current_maze), p[3], p[5]):
        raise Exception(f"Invalid door position: ({p[3]}, {p[5]})")

def p_key(p):
    'key : KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    global key_count
    key_count += 1
    if not current_maze.add_entity(Key(current_maze), p[3], p[5]):
        raise Exception(f"Invalid key position: ({p[3]}, {p[5]})")

def p_paths(p):
    'paths : PATHS LLAVE_IZQ pathList LLAVE_DER'
    p[0] = p[3]

def p_pathList(p):
    '''pathList : path pathList
                | '''
    if len(p) > 1:
        p[0] = [p[1]] + (p[2] if p[2] else [])
    else:
        p[0] = []

def p_path(p):
    '''path : PATH FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA
            | PATH LLAVE_IZQ pointList LLAVE_DER'''
    if len(p) == 14:  # Simple two-point path
        current_maze.add_path(p[4], p[6], p[10], p[12])  # Mark path on the maze grid
    else:  # Multi-point path
        points = p[3]  # List of points
        for point in points:
            current_maze.add_path(point[0], point[1])  # Mark each path point

def p_pointList(p):
    '''pointList : point pointList
                 | '''
    if len(p) > 1:
        p[0] = [p[1]] + (p[2] if p[2] else [])
    else:
        p[0] = []


def p_point(p):
    'point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    p[0] = (p[3], p[5])  # A point is represented as a tuple of two numbers


def p_enemy(p):
    'enemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA'
    position = (p[3], p[5])
    enemy_class = {"ARCHER": Archer, "WARRIOR": Warrior, "MAGE": Mage}[p[8]]
    enemy_instance = enemy_class(current_maze)
    if not current_maze.add_entity(enemy_instance, *position):
        raise Exception(f"Invalid enemy position or type at: {position} ({p[8]})")

def p_enemy_type(p):
    '''enemy_type : ARCHER
                  | WARRIOR
                  | MAGE'''
    # Assign the enemy type directly as a string
    p[0] = p[1]

def p_coin(p):
    'coin : COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    position = (p[3], p[5])
    if not current_maze.add_entity(Coin(current_maze), *position):
        raise Exception(f"Invalid coin position at: {position}")

def p_trap(p):
    'trap : TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    start = (p[3], p[5])
    end = (p[9], p[11])
    if not current_maze.add_entity(Trap(current_maze, start, end), *start):
        raise Exception(f"Invalid trap start position: {start} or end position: {end}")

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}' on line {p.lineno}" if p else "Unexpected end of input")

# Build the parser
parser = yacc.yacc()

def parse(input_string):
    global current_maze, door_count, key_count
    current_maze = None
    door_count = key_count = 0
    try:
        result = parser.parse(input_string, lexer=lexer)
        if door_count != key_count:
            raise Exception(f"Mismatch: {door_count} doors and {key_count} keys.")
        return result
    except Exception as e:
        print(e)
        return None
