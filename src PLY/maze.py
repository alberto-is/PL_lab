"""
Class to store the maze, properties and list of objects
Maze is represented as a matrix of cells, each being an object that is either path or wall and contain a list of entities
"""

import random


# ===== MAZE STRUCTURE =====

class Maze:
    """
    Store a matrix of cells, each being an object that is either path or wall and contain a list of entities.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]


    def add_entity(self, entity: "MazeObj", x: int, y: int):
        """Add an entity to the cell at (x, y)."""
        added = False  # Whether the entity was successfully added
        if 0 <= x < self.width and 0 <= y < self.height:  # Check spawn cell bounds
            cell = self.matrix[y][x]
            if cell.is_path and cell.entity is None:  # Ensure spawn cell is valid
                if not cell.is_trap_destination:  # Check if the cell is a trap destination
                    if isinstance(entity, Trap):  # Special handling for traps
                        # Validate target coordinates for traps
                        target_x, target_y = entity.target_x, entity.target_y
                        if (
                            0 <= target_x < self.width
                            and 0 <= target_y < self.height  # Check target cell bounds
                            and self.matrix[target_y][target_x].is_path
                            and self.matrix[target_y][target_x].entity is None  # Ensure target cell is valid
                        ):
                            cell.entity = entity
                            self.matrix[target_y][target_x].is_trap_destination = True  # Mark target cell as trap destination
                            entity.cell = cell
                            added = True
                        else:
                            print(f"Failed to add Trap: target cell ({target_x}, {target_y}) is invalid.")
                    else:
                        cell.entity = entity
                        entity.cell = cell
                        added = True
                else:
                    print(f"Failed to add entity {entity} at ({x}, {y}): spawn cell is a trap destination.")
            else:
                print(f"Failed to add entity {entity} at ({x}, {y}): spawn cell is not path or occupied.")
        else:
            print(f"Failed to add entity {entity} at ({x}, {y}): coordinates are out of bounds.")

        return added


    def add_room(self, x, y, room_width, room_height):
        """Set a rectangular section as path."""
        added = False
        if 0 <= x < self.width and 0 <= y < self.height:  # Check that the room starts within bounds
            if 0 <= x + room_width - 1 < self.width and 0 <= y + room_height - 1 < self.height:  # Check that the room ends within bounds
                for i in range(x, x + room_width): # x y is the top left corner of the room
                    for j in range(y, y + room_height):
                        if not self.matrix[j][i].set_path(): # Set each cell as path
                            print("Failed to add room: a cell is already path.")
                            break
                added = True
            else:
                print("Failed to add room: room exceeds maze bounds.")
        else:
            print("Failed to add room: room starts outside maze bounds.")
        return added


    def add_path(self, x1, y1, x2, y2):
        """Set a straight line of path between two points."""
        added = False
        if 0 <= x1 < self.width and 0 <= y1 < self.height:  # Check that the start point is within bounds
            if 0 <= x2 < self.width and 0 <= y2 < self.height:  # Check that the end point is within bounds
                if x1 == x2 or y1 == y2: # Check the path is straight
                    if x1 == x2:  # Vertical path
                        for y in range(min(y1, y2), max(y1, y2) + 1):
                            if not self.matrix[y][x1].set_path():
                                print(f"Failed to add path: cell ({x1}, {y}) is already path.")
                                break
                    else:  # Horizontal path
                        for x in range(min(x1, x2), max(x1, x2) + 1):
                            if not self.matrix[y1][x].set_path():
                                print(f"Failed to add path: cell ({x}, {y1}) is already path.")
                                break
                    added = True
                else:
                    print("Failed to add path: path is not straight.")
            else:
                print("Failed to add path: end point is outside maze bounds.")
        else:
            print("Failed to add path: start point is outside maze bounds.")
        return added

    
    def add_point(self, x, y):
        """Set a single cell as path."""
        added = False
        if 0 <= x < self.width and 0 <= y < self.height:
            if not self.matrix[y][x].set_path():
                print(f"Failed to add point: cell ({x}, {y}) already path.")
            else:
                added = True
        else:
            print("Failed to add point: coordinates are out of bounds.")
        return added
        

    def move_entity(self, entity: "MazeObj", dx: int, dy: int):
        """Move an entity by dx, dy."""
        old_cell = entity.cell
        new_x = old_cell.x + dx
        new_y = old_cell.y + dy
        moved = False

        if 0 <= new_x < self.width and 0 <= new_y < self.height:  # Check bounds
            new_cell = self.matrix[new_y][new_x]
            if new_cell.is_path and new_cell.entity is None:  # Ensure valid move
                # Ensure target cell is not a trap destination and the entity is not the player
                if not new_cell.is_trap_destination or isinstance(entity, Player): # Player is exempt to move into trap destinations
                    old_cell.entity = None  # Remove from old cell
                    new_cell.entity = entity  # Add to new cell
                    entity.cell = new_cell  # Update entity's reference
                    moved = True  # Movement succeeded
                else:
                    print("Failed to move entity: target cell is a trap destination.")
            else:
                print("Failed to move entity: target cell is invalid or occupied.")
        else:
            print("Failed to move entity: target coordinates are out of bounds.")
        return moved

    
    def teleport_entity(self, entity: "MazeObj", x: int, y: int):
        """
        Abruptly move an entity to a new location without adding increments.
        """
        old_cell = entity.cell
        new_cell = self.matrix[y][x]
        teleported = False  # Whether the teleport succeeded

        if new_cell.is_path and new_cell.entity is None:  # Ensure valid teleport
            if not new_cell.is_trap_destination or isinstance(entity, Player):
                old_cell.entity = None  # Remove from old cell
                new_cell.entity = entity  # Add to new cell
                entity.cell = new_cell  # Update entity's reference
                teleported = True  # Teleport succeeded
            else:
                print("Failed to teleport entity: target cell is a trap destination.")
        else:
            print("Failed to teleport entity: target cell is invalid or occupied.")
        return teleported
    

    def print(self):
        """Print the maze to the console."""
        for row in self.matrix:
            for cell in row:
                if cell.entity is not None:
                    print(cell.entity, end=" ")
                else:
                    print("." if cell.is_path else "#", end=" ")
            print()  # Newline at the end of each row
        

class Cell:
    """
    Store the properties of a cell.
    """
    def __init__(self, x, y, is_path=False, is_trap_destination=False):
        self.x = x  # Store the cell's x-coordinate in the maze
        self.y = y  # Store the cell's y-coordinate in the maze
        self.is_path = is_path
        self.entity = None  # Reference to the contained entity, if any
        self.is_trap_destination = is_trap_destination  # Whether the cell is the target of a trap


    def set_path(self):
        """Set the cell as path."""
        set_as_path = False  # Whether the cell was successfully set as path
        if not self.is_path:
            self.is_path = True
            set_as_path = True
        return set_as_path


    def set_trap_destination(self):
        """Set the cell as a trap destination."""
        set_as_trap_destination = False
        if self.is_path:  # Only path cells can be trap destinations
            set_as_trap_destination = True  # Set the cell as a trap destination
        return set_as_trap_destination


# ===== OBJECTS =====

class MazeObj:
    """
    Base class for objects in the maze.
    """
    def __init__(self, maze):
        self.maze = maze
        self.cell = None  # Reference to the cell the object occupies
        self.pushable = False  # Whether the object can be pushed by an arrow
    

class Player(MazeObj):  # When creating the player, use ENTRY token as the position to create it at
    """
    Class to represent the player entity.
    Players can move and must reach an exit to win.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.keys = 0  # Number of keys the player has
        self.pushable = True

    
    def __str__(self):
        return "P"  # Representation of the player in console


class Exit(MazeObj):
    """
    Class to represent the exit entity.
    Exits are the goal of the game and the player must reach one to win.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = False
    

    def __str__(self):
        return "E"  # Representation of the exit in console


class Bomb(MazeObj):
    """
    Class to represent the bomb entity.
    Bombs work like mines, exploding when the player steps in the 8 surrounding squares, wasting a turn.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = True
    

    def __str__(self):
        return "B"  # Representation of the bomb in console


class Coin(MazeObj):
    """
    Class to represent the coin entity.
    Coins can be collected by the player to return a turn.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = True
    

    def __str__(self):
        return "C"  # Representation of the coin in console


class Key(MazeObj):
    """
    Class to represent the key entity.
    Keys can be collected by the player to unlock doors.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = True
    

    def __str__(self):
        return "K"  # Representation of the key in console


class Door(MazeObj):
    """
    Class to represent the door entity.
    Doors block the player's advances until a key is used to unlock them.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = False
    

    def __str__(self):
        return "D"  # Representation of the door in console


class Trap(MazeObj):
    """
    A trap that teleports the player to a specific location.
    """
    def __init__(self, maze, target_x, target_y):
        super().__init__(maze)
        self.target_x = target_x
        self.target_y = target_y
        self.pushable = False


    def __str__(self):
        return "T"


    def activate(self, player):
        """
        Activate the trap, teleporting the player to the target location.
        """
        if 0 <= self.target_x < self.maze.width and 0 <= self.target_y < self.maze.height:
            target_cell = self.maze.matrix[self.target_y][self.target_x]
            if target_cell.is_path and target_cell.entity is None:  # Ensure valid teleport destination
                self.maze.move_entity(player, self.target_x - player.cell.x, self.target_y - player.cell.y)
            else:
                print("Teleport failed: target cell is invalid or occupied.")
        else:
            print("Teleport failed: target coordinates are out of bounds.")


class Warrior(MazeObj):
    """
    Class to represent the warrior enemy.
    Warriors block player's advances and must be defeated to pass, wasting a turn.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = True
    

    def __str__(self):
        return "W"  # Representation of the warrior in console


class Mage(MazeObj):
    """
    Class to represent the mage enemy.
    Mages pick a random location every few turns to spawn a new bomb there, each mage can spawn up to 5 bombs.
    """

    def __init__(self, maze):
        super().__init__(maze)
        self.bombs_spawned = 0
        self.pushable = True
    

    def __str__(self):
        return "M"  # Representation of the mage in console


    def spawn_bomb(self):
        """
        Spawn a bomb at the randomly chosen location.
        """
        spawned = False  # Whether the bomb was successfully spawned
        if self.bombs_spawned < 5:
            # Find a random empty cell
            empty_cells = []
            for row in self.maze.matrix:
                for cell in row:
                    if cell.is_path and cell.entity is None:
                        empty_cells.append(cell)
            if empty_cells:
                bomb_cell = random.choice(empty_cells)
                self.maze.add_entity(Bomb(self.maze), bomb_cell.x, bomb_cell.y)
                self.bombs_spawned += 1
                spawned = True
            else:
                print("Failed to spawn bomb: no empty cells left.")
        else:
            print("Failed to spawn bomb: maximum bombs spawned.")
        return spawned


class Archer(MazeObj):
    """
    Archer enemy that shoots arrows to push certain objects.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.pushable = True


    def __str__(self):
        return "A"


    def shoot(self):
        """
        Shoot an arrow in a random direction.
        """
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        shoot = False # Whether the archer successfully shot an arrow

        # Determine the target cell based on the direction
        dx, dy = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }[direction]

        x, y = self.cell.x, self.cell.y
        target_x, target_y = x + dx, y + dy

        if 0 <= target_x < self.maze.width and 0 <= target_y < self.maze.height:  # Check bounds
            target_cell = self.maze.matrix[target_y][target_x]
            if target_cell.is_path and target_cell.entity is None:  # Ensure valid target to spawn arrow
                arrow = Arrow(self.maze, direction, self)
                self.maze.add_entity(arrow, target_x, target_y)
                shoot = True
            else:
                print("Failed to shoot arrow: target cell is invalid or occupied.")
        else:
            print("Failed to shoot arrow: target coordinates are out of bounds.")
        return shoot


# ===== AUXILIARY OBJECTS NOT DEFINED IN LANGUAGE =====

class Arrow(MazeObj):
    """
    Class to represent the arrow entity.
    Arrows move in a given direction and knock back objects if they collide.
    """
    def __init__(self, maze, direction, archer):
        super().__init__(maze)
        self.direction = direction  # Direction as a string: "up", "down", "left", "right"
        self.archer = archer  # Reference to the archer that shot it
        self.pushable = False
        self.can_move = False  # Start unable to move until the player has had a turn

    def __str__(self):
        return {
            "up": "↑",
            "down": "↓",
            "left": "←",
            "right": "→"
        }.get(self.direction, "?")  # Represent the arrow's direction