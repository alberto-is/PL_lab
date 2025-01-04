
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ARCHER BOMB COIN COMA DIMENSIONS DOOR ENEMY ENTRY EXIT FROM KEY LLAVE_DER LLAVE_IZQ MAGE MAZE NUMBER OBSTACLES PAREN_DER PAREN_IZQ PATH PATHS POINT PUNTO_COMA ROOM ROOMS TO TRAP TYPE WARRIOR Xprogram : levellevel : maze entry exit rooms paths obstaclesmaze : MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMAdimensions : DIMENSIONS NUMBER X NUMBERentry : ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMAexit : EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMArooms : ROOMS LLAVE_IZQ roomList LLAVE_DERroomList : room roomList\n                | room : ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions LLAVE_DERobstacles : OBSTACLES LLAVE_IZQ obstacleList LLAVE_DERobstacleList : obstacle obstacleList\n                    | obstacle : bomb\n                | enemy\n                | door\n                | key\n                | coin\n                | trapbomb : BOMB PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMAdoor : DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMAkey : KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMApaths : PATHS LLAVE_IZQ pathList LLAVE_DERpathList : path pathList\n                | path : PATH FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA\n            | PATH LLAVE_IZQ pointList LLAVE_DERpointList : point pointList\n                 | point : POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMAenemy : ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMAenemy_type : ARCHER\n                  | WARRIOR\n                  | MAGEcoin : COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMAtrap : TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA'
    
_lr_action_items = {'MAZE':([0,],[4,]),'$end':([1,2,26,65,],[0,-1,-2,-11,]),'ENTRY':([3,24,],[6,-3,]),'LLAVE_IZQ':([4,14,20,27,38,],[7,21,28,35,61,]),'EXIT':([5,64,],[9,-5,]),'PAREN_IZQ':([6,9,41,52,53,54,55,56,57,60,76,122,123,],[10,15,62,67,68,69,70,71,72,73,88,130,131,]),'DIMENSIONS':([7,107,],[12,12,]),'ROOMS':([8,78,],[14,-6,]),'NUMBER':([10,12,15,23,25,32,62,67,68,69,70,71,72,73,88,89,90,91,92,93,94,95,96,106,130,131,136,137,],[16,18,22,33,34,42,77,79,80,81,82,83,84,85,97,98,99,100,101,102,103,104,105,115,134,135,138,139,]),'LLAVE_DER':([11,21,28,29,30,34,35,36,37,40,44,45,46,47,48,49,50,51,59,61,66,74,75,86,87,116,117,119,120,121,125,132,133,142,143,],[17,-9,-25,39,-9,-4,-13,58,-25,-8,65,-13,-14,-15,-16,-17,-18,-19,-24,-29,-12,86,-29,-27,-28,125,-20,-21,-22,-35,-10,-30,-31,-36,-26,]),'PATHS':([13,39,],[20,-7,]),'COMA':([16,22,77,79,80,81,82,83,84,85,97,134,135,],[23,32,89,90,91,92,93,94,95,96,106,136,137,]),'PUNTO_COMA':([17,43,63,108,110,111,112,124,126,127,128,129,140,141,],[24,64,78,117,119,120,121,132,133,-32,-33,-34,142,143,]),'X':([18,],[25,]),'OBSTACLES':([19,58,],[27,-23,]),'ROOM':([21,30,125,],[31,31,-10,]),'PATH':([28,37,86,143,],[38,38,-27,-26,]),'FROM':([31,38,],[41,60,]),'PAREN_DER':([33,42,98,99,100,101,102,103,104,105,115,138,139,],[43,63,107,108,109,110,111,112,113,114,124,140,141,]),'BOMB':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[52,52,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'ENEMY':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[53,53,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'DOOR':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[54,54,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'KEY':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[55,55,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'COIN':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[56,56,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'TRAP':([35,45,46,47,48,49,50,51,117,119,120,121,133,142,],[57,57,-14,-15,-16,-17,-18,-19,-20,-21,-22,-35,-31,-36,]),'POINT':([61,75,132,],[76,76,-30,]),'TYPE':([109,],[118,]),'TO':([113,114,],[122,123,]),'ARCHER':([118,],[127,]),'WARRIOR':([118,],[128,]),'MAGE':([118,],[129,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'level':([0,],[2,]),'maze':([0,],[3,]),'entry':([3,],[5,]),'exit':([5,],[8,]),'dimensions':([7,107,],[11,116,]),'rooms':([8,],[13,]),'paths':([13,],[19,]),'obstacles':([19,],[26,]),'roomList':([21,30,],[29,40,]),'room':([21,30,],[30,30,]),'pathList':([28,37,],[36,59,]),'path':([28,37,],[37,37,]),'obstacleList':([35,45,],[44,66,]),'obstacle':([35,45,],[45,45,]),'bomb':([35,45,],[46,46,]),'enemy':([35,45,],[47,47,]),'door':([35,45,],[48,48,]),'key':([35,45,],[49,49,]),'coin':([35,45,],[50,50,]),'trap':([35,45,],[51,51,]),'pointList':([61,75,],[74,87,]),'point':([61,75,],[75,75,]),'enemy_type':([118,],[126,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> level','program',1,'p_program','parser.py',12),
  ('level -> maze entry exit rooms paths obstacles','level',6,'p_level','parser.py',16),
  ('maze -> MAZE LLAVE_IZQ dimensions LLAVE_DER PUNTO_COMA','maze',5,'p_maze','parser.py',35),
  ('dimensions -> DIMENSIONS NUMBER X NUMBER','dimensions',4,'p_dimensions','parser.py',41),
  ('entry -> ENTRY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','entry',7,'p_entry','parser.py',45),
  ('exit -> EXIT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','exit',7,'p_exit','parser.py',50),
  ('rooms -> ROOMS LLAVE_IZQ roomList LLAVE_DER','rooms',4,'p_rooms','parser.py',55),
  ('roomList -> room roomList','roomList',2,'p_roomList','parser.py',59),
  ('roomList -> <empty>','roomList',0,'p_roomList','parser.py',60),
  ('room -> ROOM FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER dimensions LLAVE_DER','room',9,'p_room','parser.py',64),
  ('obstacles -> OBSTACLES LLAVE_IZQ obstacleList LLAVE_DER','obstacles',4,'p_obstacles','parser.py',69),
  ('obstacleList -> obstacle obstacleList','obstacleList',2,'p_obstacleList','parser.py',73),
  ('obstacleList -> <empty>','obstacleList',0,'p_obstacleList','parser.py',74),
  ('obstacle -> bomb','obstacle',1,'p_obstacle','parser.py',78),
  ('obstacle -> enemy','obstacle',1,'p_obstacle','parser.py',79),
  ('obstacle -> door','obstacle',1,'p_obstacle','parser.py',80),
  ('obstacle -> key','obstacle',1,'p_obstacle','parser.py',81),
  ('obstacle -> coin','obstacle',1,'p_obstacle','parser.py',82),
  ('obstacle -> trap','obstacle',1,'p_obstacle','parser.py',83),
  ('bomb -> BOMB PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','bomb',7,'p_bomb','parser.py',87),
  ('door -> DOOR PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','door',7,'p_door','parser.py',92),
  ('key -> KEY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','key',7,'p_key','parser.py',99),
  ('paths -> PATHS LLAVE_IZQ pathList LLAVE_DER','paths',4,'p_paths','parser.py',106),
  ('pathList -> path pathList','pathList',2,'p_pathList','parser.py',110),
  ('pathList -> <empty>','pathList',0,'p_pathList','parser.py',111),
  ('path -> PATH FROM PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','path',14,'p_path','parser.py',118),
  ('path -> PATH LLAVE_IZQ pointList LLAVE_DER','path',4,'p_path','parser.py',119),
  ('pointList -> point pointList','pointList',2,'p_pointList','parser.py',128),
  ('pointList -> <empty>','pointList',0,'p_pointList','parser.py',129),
  ('point -> POINT PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','point',7,'p_point','parser.py',137),
  ('enemy -> ENEMY PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TYPE enemy_type PUNTO_COMA','enemy',9,'p_enemy','parser.py',142),
  ('enemy_type -> ARCHER','enemy_type',1,'p_enemy_type','parser.py',150),
  ('enemy_type -> WARRIOR','enemy_type',1,'p_enemy_type','parser.py',151),
  ('enemy_type -> MAGE','enemy_type',1,'p_enemy_type','parser.py',152),
  ('coin -> COIN PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','coin',7,'p_coin','parser.py',157),
  ('trap -> TRAP PAREN_IZQ NUMBER COMA NUMBER PAREN_DER TO PAREN_IZQ NUMBER COMA NUMBER PAREN_DER PUNTO_COMA','trap',13,'p_trap','parser.py',163),
]
