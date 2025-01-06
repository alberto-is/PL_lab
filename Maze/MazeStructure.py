# Archivo generado desde JAVA, NO MODIFICAR

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

maze = MazeStructure(
	(10, 10),
	(0, 0),
	(9, 9),
	[
		(1, 1),
		(1, 2),
		(1, 3),
		(2, 1),
		(2, 2),
		(2, 3),
		(3, 1),
		(3, 2),
		(3, 3),
		(5, 5),
		(5, 6),
		(6, 5),
		(6, 6),
		(0, 0),
		(1, 0),
		(2, 0),
		(3, 0),
		(4, 0),
		(5, 0),
		(6, 0),
		(7, 0),
		(8, 0),
		(9, 0),
		(9, 1),
		(9, 2),
		(9, 3),
		(9, 4),
		(9, 5),
		(9, 6),
		(9, 7),
		(9, 8),
		(9, 9),
		(4, 4),
		(3, 4),
		(4, 5),
	],
	[
		Obstacle('BOMB', (2, 1)),
		Obstacle('ENEMY', (3, 3),enemy_type='archer'),
		Obstacle('DOOR', (1, 1)),
		Obstacle('KEY', (6, 6)),
		Obstacle('TRAP', (5, 5), (5, 6)),
		Obstacle('COIN', (4, 4)),
	],
)

