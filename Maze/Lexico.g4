// lexico de nuestro lenguaje
lexer grammar Lexico;

MAZE: 'maze';
DIMENSIONS: 'dimensions';
ENTRY: 'entry';
EXIT: 'exit';
ROOMS: 'rooms';
ROOM: 'room';
FROM: 'from';
TO: 'to';
PATH: 'path';
PATHS: 'paths';
POINT: 'point';
OBSTACLES: 'obstacles';
BOMB: 'bomb';
ENEMY: 'enemy';
DOOR: 'door';
KEY: 'key';
COIN: 'coin';
TRAP: 'trap';
TYPE: 'type';
ARCHER: 'archer';
WARRIOR: 'warrior';
MAGE: 'mage';
X: 'x';

NUMBER: [0] | [1-9][0-9]*;
      
// Symbols
PAREN_IZQ: '(';
PAREN_DER: ')';
LLAVE_IZQ: '{';
LLAVE_DER: '}';
COMA: ',';
PUNTO_COMA: ';';

// espacios en blanco y comentarios
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
COMMENT: '/*' .*? '*/' -> skip;