
grammar maze;

import Lexico;
// reglas sintacticas
program: level EOF;

level: maze entry exit rooms paths obstacles;

maze: MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA;

dimensions: DIMENSIONS number X number;
    
entry: ENTRY PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

exit: EXIT PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

rooms: ROOMS LLAVE_IZQ roomList LLAVE_DER;

roomList: room roomList 
        | ;

room: ROOM ID FROM PAREN_IZQ number COMA number PAREN_DER dimensions LLAVE_IZQ obstacleList LLAVE_DER;

obstacleList: obstacle obstacleList 
            | ;

obstacle: bomb 
        | enemy 
        | door 
        | key 
        | coin 
        | trap;

bomb: BOMB PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

enemy: ENEMY PAREN_IZQ number COMA number PAREN_DER TYPE enemy_type PUNTO_COMA;

door: DOOR PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

key: KEY PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

coin: COIN PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

trap: TRAP PAREN_IZQ number COMA number PAREN_DER TO PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

enemy_type: ARCHER 
        | WARRIOR 
        | MAGE;

paths: PATHS LLAVE_IZQ pathList LLAVE_DER;

pathList: path pathList 
        | ;

path: PATH FROM PAREN_IZQ number COMA number PAREN_DER TO PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA
    | PATH LLAVE_IZQ pointList LLAVE_DER;

pointList: point pointList | ;

point: POINT PAREN_IZQ number COMA number PAREN_DER PUNTO_COMA;

obstacles: OBSTACLES LLAVE_IZQ obstacleList LLAVE_DER;

number: NUMBER;


/*
tipos de errores
- numeros negativos
- un numero no puede empezar por 0<numero>
- caracter * no reconocido, ¿querias usar x?
- linea de comentario no formado correctamente
- caracter no valido
*/


