import lexer
import ply.yacc as yacc
from maze import Maze, Entity, Door, Key, Coin, Trap, Exit, Archer, Warrior, Mage, Bomb

# Lista de nombres de tokens - es importante que coincidan exactamente con los usados en el lexer
tokens = lexer.tokens

# Símbolos de inicio
start = 'maze'

# Gramáticas
# maze -> 'maze' '{' dimensions; entry; exit; rooms; paths; obstacles '}'
def p_maze(p):
    'maze : MAZE LLLAVE_IZQ dimensions SEMICOLON entry SEMICOLON exit SEMICOLON rooms SEMICOLON paths SEMICOLON obstacles LLLAVE_DER'
    p[0] = p[3]

# dimensions -> 'dimensions' NUMBER 'x' NUMBER
def p_dimensions(p):
    'dimensions : DIMENSIONS NUMBER X NUMBER'
    maze = Maze(p[2], p[4])
    p[0] = maze

# entry -> 'entry' '(' NUMBER ',' NUMBER ')'
def p_entry(p):
    'entry : ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER'
    if not p[0].add_entity(Exit(p[0]), p[3], p[5]):
        raise Exception("INVALID MAZE: Invalid entry")

# exit -> 'exit' '(' NUMBER ',' NUMBER ')'
def p_exit(p):
    'exit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER'
    if not p[0].add_entity(Exit(p[0]), p[3], p[5]):
        raise Exception("INVALID MAZE: Invalid exit")

# rooms -> 'rooms' '{' room* '}'
def p_rooms(p):
    'rooms : ROOMS LLLAVE_IZQ room_list LLLAVE_DER'
    p[0] = p[0]

# room_list -> room*
def p_room_list(p):
    '''room_list : 
                 | room_list room'''
    pass

# room -> 'room' 'from' '(' NUMBER ',' NUMBER ')' 'dimensions' NUMBER 'x' NUMBER '{' entity* '}'
def p_room(p):
    'room : ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER DIMENSIONS NUMBER X NUMBER LLLAVE_IZQ entity_list LLLAVE_DER'
    if not p[0].add_room(p[0], p[4], p[6], p[10], p[12]):
        raise Exception("INVALID MAZE: Invalid room")
    p[0] = p[0]

# entity_list -> entity*
def p_entity_list(p):
    '''entity_list : 
                     | entity_list entity'''
    pass

# entity -> 'type' | 'door' | 'key' | 'trap' | 'coin' | 'bomb' | 'archer' | 'warrior' | 'mage'
def p_entity(p):
    '''entity : TYPE 
               | DOOR 
               | KEY 
               | TRAP 
               | COIN 
               | BOMB 
               | ARCHER 
               | WARRIOR 
               | MAGE'''
    match p[1]:
        case 'type':
            entity = Entity(p[0])
        case 'door':
            entity = Door(p[0])
        case 'key':
            entity = Key(p[0])
        case 'trap':
            entity = Trap(p[0])
        case 'coin':
            entity = Coin(p[0])
        case 'bomb':
            entity = Bomb(p[0])
        case 'archer':
            entity = Archer(p[0])
        case 'warrior':
            entity = Warrior(p[0])
        case 'mage':
            entity = Mage(p[0])
        case _: 
            raise Exception("INVALID MAZE: Invalid entity")

    if not p[0].add_entity(entity, p[0].last_room.x, p[0].last_room.y):
        raise Exception("INVALID MAZE: Invalid entity")

# paths -> 'paths' '{' path* '}'
def p_paths(p):
    'paths : PATHS LLLAVE_IZQ path_list LLLAVE_DER'
    p[0] = p[0]

# path_list -> path*
def p_path_list(p):
    '''path_list : 
                  | path_list path'''
    pass

# path -> 'path' 'from' '(' NUMBER ',' NUMBER ')' 'to' '(' NUMBER ',' NUMBER ')'
def p_path(p):
    '''path : PATH FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER 
             | PATH LLLAVE_IZQ point_list RLLAVE_DER'''
    if len(p) == 11:
        if not p[0].add_path(p[4], p[6], p[9], p[11]):
            raise Exception("INVALID MAZE: Invalid path")
    else:
        p[0] = p[0]

# point_list -> point*
def p_point_list(p):
    '''point_list : 
                   | point_list point'''
    pass

# point -> 'point' '(' NUMBER ',' NUMBER ')'
def p_point(p):
    'point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER'
    if not p[0].add_point(p[4], p[6]):
        raise Exception("INVALID MAZE: Invalid point")

# obstacles -> 'obstacles' '{' obstacle* '}'
def p_obstacles(p):
    'obstacles : OBSTACLES LLLAVE_IZQ obstacle_list LLLAVE_DER'
    if p[0].num_doors != p[0].num_keys:
        raise Exception("INVALID MAZE: Number of doors and keys does not match")
    p[0] = p[0]

# obstacle_list -> obstacle*
def p_obstacle_list(p):
    '''obstacle_list : 
                      | obstacle_list obstacle'''
    pass

# obstacle -> 'coin' | 'bomb' | 'archer' | 'warrior' | 'mage' | 'door' | 'key' | 'trap'
def p_obstacle(p):
    '''obstacle : COIN 
                 | BOMB 
                 | ARCHER 
                 | WARRIOR 
                 | MAGE 
                 | DOOR 
                 | KEY 
                 | TRAP'''
    match p[1]:
        case 'coin':
            entity = Coin(p[0])
        case 'bomb':
            entity = Bomb(p[0])
        case 'archer':
            entity = Archer(p[0])
        case 'warrior':
            entity = Warrior(p[0])
        case 'mage':
            entity = Mage(p[0])
        case 'door':
            entity = Door(p[0])
        case 'key':
            entity = Key(p[0])
        case 'trap':
            entity = Trap(p[0])
        case _:
            raise Exception("INVALID MAZE: Invalid obstacle")
    if not p[0].add_entity(entity, p[0].width // 2, p[0].height // 2):
        raise Exception("INVALID MAZE: Invalid obstacle")

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}: token '{p.value}'")
    else:
        print(f"Syntax error at EOF")

# Create the parser
parser = yacc.yacc()

# Example usage
if __name__ == "__main__":
    with open("ej_maze_correcto.txt", "r") as f:
        s = f.read()
    maze = parser.parse(s)
    print(maze)