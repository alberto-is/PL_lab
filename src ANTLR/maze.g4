
grammar maze;

import Lexico;
// reglas sintacticas
program: level EOF;

level: maze entry exit rooms paths obstacles;

maze: MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA;

dimensions: DIMENSIONS number X number # gobal_dim;
    
entry: ENTRY PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_entry;

exit: EXIT PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_exit;

rooms: ROOMS LLAVE_IZQ roomList LLAVE_DER;

roomList: room roomList 
        | ;

room: ROOM FROM PAREN_IZQ number COMA number PAREN_DER dimensions PUNTO_COMA # dim_room;

obstacleList: obstacle obstacleList 
            | ;

obstacle: bomb 
        | enemy 
        | door 
        | key 
        | coin 
        | trap;

bomb: BOMB PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_bomb;

enemy: ENEMY PAREN_IZQ number COMA number PAREN_DER TYPE enemy_type PUNTO_COMA # cord_enemy;

door: DOOR PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_door;

key: KEY PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_key;

coin: COIN PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_coin;

trap: TRAP PAREN_IZQ number COMA number PAREN_DER TO PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_trap;

enemy_type: ARCHER 
        | WARRIOR 
        | MAGE;

paths: PATHS LLAVE_IZQ pathList LLAVE_DER;

pathList: path pathList 
        | ;

path: PATH FROM PAREN_IZQ number COMA number PAREN_DER TO PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_path
    | PATH LLAVE_IZQ pointList LLAVE_DER # cord_point_list
    ;

pointList: point pointList | ;

point: POINT PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA # cord_point;

obstacles: OBSTACLES LLAVE_IZQ obstacleList LLAVE_DER;

number: NUMBER # num;



