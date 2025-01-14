# Archivo generado desde JAVA, ¡NO MODIFICAR!

class Obstacle:
	def __init__(self, type, position, destination=None, enemy_type=None):
		self.type = type
		self.enemy_type = enemy_type
		self.position = position
		self.destination = destination

class MazeStructure:
	def __init__(self, dimensions, entry, exit, list_points_path, list_obstacles):
		self.dimensions = dimensions
		self.entry = entry
		self.exit = exit
		self.list_points_path = list_points_path
		self.list_obstacles = list_obstacles

# Crear el objeto MazeStructure
maze_structure = MazeStructure(
	(9, 9),
	(8, 4),
	(4, 0),
	[
		(0, 0),
		(0, 1),
		(1, 0),
		(1, 1),
		(0, 7),
		(0, 8),
		(1, 7),
		(1, 8),
		(3, 3),
		(3, 4),
		(3, 5),
		(4, 3),
		(4, 4),
		(4, 5),
		(5, 3),
		(5, 4),
		(5, 5),
		(3, 0),
		(4, 0),
		(5, 0),
		(8, 3),
		(8, 4),
		(8, 5),
		(4, 1),
		(4, 2),
		(6, 4),
		(7, 4),
		(1, 2),
		(1, 3),
		(1, 4),
		(1, 5),
		(1, 6),
		(2, 4),
	],
	[
		Obstacle('DOOR', (2, 4)),
		Obstacle('BOMB', (1, 2)),
		Obstacle('ENEMY', (0, 0),enemy_type='archer'),
		Obstacle('ENEMY', (0, 8),enemy_type='mage'),
		Obstacle('TRAP', (1, 8), (4, 1)),
		Obstacle('ENEMY', (4, 4),enemy_type='warrior'),
		Obstacle('KEY', (5, 3)),
		Obstacle('COIN', (1, 4)),
	],
)

