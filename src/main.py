import os
import time
from maze import *


def update_display(maze):
    """
    Update the display by clearing the console and printing the maze
    """
    global TURNS_TO_ESCAPE
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Print the maze
    maze.print()
    print(f"Total turns: {TURNS_TO_ESCAPE}")


def update_entity_list(maze):
    """
    Update the list of entities in the maze
    """
    maze_entities = []
    for x in range(maze.width):
        for y in range(maze.height):
            if maze.matrix[x][y].entity is not None:
                maze_entities.append(maze.matrix[x][y].entity)
    return maze_entities


def update_arrows(maze, maze_entities):
    """
    Update the arrows in the maze, moving them and checking for collisions
    """
    for entity in maze_entities:
        if isinstance(entity, Arrow):
            # Check direction (up, down, left, right)
            if entity.direction == "up":
                dx = 0
                dy = -1
            elif entity.direction == "down":
                dx = 0
                dy = 1
            elif entity.direction == "left":
                dx = -1
                dy = 0
            elif entity.direction == "right":
                dx = 1
                dy = 0
            
            # Check if the arrow is allowed to move (can_move = True)
            if entity.can_move:
                # Move the arrow
                if not maze.move_entity(entity, dx, dy):  # A collision has been detected
                    target_cell_x = entity.cell.x + dx
                    target_cell_y = entity.cell.y + dy
                    # Ensure the target cell is within the bounds
                    if 0 <= target_cell_x < maze.width and 0 <= target_cell_y < maze.height:
                        target_cell = maze.matrix[target_cell_y][target_cell_x]
                            
                        # Check if we hit a movable entity (pushable object)
                        if target_cell.entity is not None and target_cell.entity.pushable:
                            # Move the entity (pushable)
                            if maze.move_entity(target_cell.entity, dx, dy):
                                print(f"Arrow pushed {target_cell.entity} to ({target_cell_x + dx}, {target_cell_y + dy})")
                            else:
                                print(f"Arrow hit a pushable object, but couldn't move it.")
                        else:
                            # Arrow hit a wall or non-pushable object
                            print(f"Arrow hit a wall or non-pushable object at ({target_cell_x}, {target_cell_y})")
                        
                    # Remove the arrow from the maze regardless of what it hit
                    entity.cell.entity = None
    update_display(maze)


def move_player(maze, maze_entities):
    """
    Move the player in the maze and handle collisions with other entities
    """
    player = None
    moved = False
    win = False
    global TURNS_TO_ESCAPE
    for entity in maze_entities:
        if isinstance(entity, Player):
            player = entity
            break

    while not moved:  # Keep asking for input until the player moves
        if player is not None:
            direction = input("Enter direction (wasd): ")  #FIXME: TEMP MOVEMENT INPUT. IMPLEMENT ACTUAL KEYS INPUT
        dx = 0
        dy = 0
        if direction == "w":
            dy = -1
        elif direction == "s":
            dy = 1
        elif direction == "a":
            dx = -1
        elif direction == "d":
            dx = 1

        if maze.move_entity(player, dx, dy):
            moved = True
            TURNS_TO_ESCAPE += 1   
        else:  # Check what we hit
            target_cell_x = player.cell.x + dx
            target_cell_y = player.cell.y + dy
            target_cell = maze.matrix[target_cell_y][target_cell_x]

            # Check if it failed due to hitting the exit
            if target_cell.entity is not None and isinstance(target_cell.entity, Exit):
                TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                target_cell.entity = None  # Remove the exit from the maze
                maze.move_entity(player, dx, dy)  # Redo the move
                moved = True
                update_display(maze)
                win = True
                break
                

            # Check if it failed due to hitting a coin
            if target_cell.entity is not None and isinstance(target_cell.entity, Coin):
                TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                TURNS_TO_ESCAPE -= 3  # Reduce turn count by 3 (value of coin)
                target_cell.entity = None  # Remove the coin from the maze
                maze.move_entity(player, dx, dy) # Redo the move
                moved = True
                update_display(maze)

            # Check if it failed due to hitting a key
            if target_cell.entity is not None and isinstance(target_cell.entity, Key):
                TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                player.keys += 1  # Give the player a key
                target_cell.entity = None  # Remove the key from the maze
                maze.move_entity(player, dx, dy) # Redo the move
                moved = True
                update_display(maze)

            # Check if it failed due to hitting a door
            if target_cell.entity is not None and isinstance(target_cell.entity, Door):
                # Check if we have a key
                if player.keys > 0:
                    player.keys -= 1  # Use a key
                    TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                    target_cell.entity = None  # Remove the door from the maze
                    maze.move_entity(player, dx, dy) # Redo the move
                    moved = True
                    update_display(maze)
                else:
                    print("Player hit a door without a key")
                    update_display(maze)

            # Check if it failed due to hitting a trap
            if target_cell.entity is not None and isinstance(target_cell.entity, Trap):
                if maze.teleport_entity(player, target_cell.entity.target_x, target_cell.entity.target_y):
                    print("Player hit a trap and teleported")
                    TURNS_TO_ESCAPE += 1  # Increment the turn count because move is valid
                    moved = True
                    update_display(maze)
                else:  # Target is blocked
                    print("Player hit a trap but couldn't teleport. Exit blocked by something")
                    update_display(maze)

            # Check if it failed due to hitting a warrior
            if target_cell.entity is not None and isinstance(target_cell.entity, Warrior):
                print("Warrior collision")
                target_cell.entity = None  # Kill enemy
                TURNS_TO_ESCAPE += 2  # 2 turns, one for the move, one because it was a warrior
                print("Player hit a warrior and killed it")
                moved = True
                update_display(maze)

            # Check if it failed due to hitting an archer or mage
            if target_cell.entity is not None and (isinstance(target_cell.entity, Archer) or isinstance(target_cell.entity, Mage)):
                print("Player hit an archer or mage")
                target_cell.entity = None  # Kill enemy
                TURNS_TO_ESCAPE += 1
                maze.move_entity(player, dx, dy)  # Redo the move
                moved = True
                update_display(maze)


            # Check if it failed due to hitting an arrow
            if target_cell.entity is not None and isinstance(target_cell.entity, Arrow):
                target_cell.entity = None  # Tank the arrow but don't move, wasting a turn
                TURNS_TO_ESCAPE += 1
                moved = True
                print("Player hit an arrow and tanked it")
                update_display(maze)

            # Check if it failed due to hitting a bomb
            if target_cell.entity is not None and isinstance(target_cell.entity, Bomb):
                update_bombs(maze, maze_entities)
                update_display(maze)
                moved = True

    # Update arrows to allow movement
    for entity in maze_entities:
        if isinstance(entity, Arrow):
            entity.can_move = True
    update_display(maze)
    return win


def update_bombs(maze, maze_entities):
    """
    Update the bombs in the maze, checking for players in range to detonate
    """
    global TURNS_TO_ESCAPE
    for entity in maze_entities:
        if isinstance(entity, Bomb):
            surrounding_cells = []
            for dx in range(-1, 2):  # Get all surrounding cells
                for dy in range(-1, 2):
                    if 0 <= entity.cell.x + dx < maze.width and 0 <= entity.cell.y + dy < maze.height:
                        surrounding_cells.append(maze.matrix[entity.cell.y + dy][entity.cell.x + dx])
            # Check if player is on the bomb
            for cell in surrounding_cells:
                if cell.entity is not None and isinstance(cell.entity, Player):
                    entity.cell.entity = None  # Remove the bomb
                    TURNS_TO_ESCAPE += 3  # 3 turns, one for the move, two because it was a bomb
                    print("Bomb hit player and exploded")
    update_display(maze)


def move_enemies(maze, maze_entities):
    """
    Move the enemies in the maze randomly
    """
    for entity in maze_entities:  # Locate all enemies
        if isinstance(entity, Warrior) or isinstance(entity, Archer) or isinstance(entity, Mage):
            direction = random.choice(["up", "down", "left", "right"])
            if direction == "up":
                dx = 0
                dy = -1
            elif direction == "down":
                dx = 0
                dy = 1
            elif direction == "left":
                dx = -1
                dy = 0
            elif direction == "right":
                dx = 1
                dy = 0

            if maze.move_entity(entity, dx, dy):
                break
            else:
                print(f"{entity} failed to move to {dx}, {dy}")
    update_display(maze)


def shoot_arrows(maze, maze_entities):
    """
    Create new arrows from archers
    """
    for entity in maze_entities:
        if isinstance(entity, Archer):
            # Decide if the archer will shoot (1/5 chance)
            if random.randint(1, 5) == 1:
                # Shoot an arrow
                if not entity.shoot():
                    print("Failed to shoot arrow")
                update_display(maze) 


def summon_bombs(maze, maze_entities):
    """
    Create new bombs from mages
    """
    for entity in maze_entities:
        if isinstance(entity, Mage):
            # Decide if the mage will spawn a bomb (1/5 chance)
            if random.randint(1, 5) == 1:
                entity.spawn_bomb()
                update_display(maze)


TURNS_TO_ESCAPE = 0  # Number of turns used to escape the maze (global variable)
def main():
    SLEEP_TIME = 0.2  # Time to sleep between each turn
    # Create a test maze and print it
    maze = Maze(11, 11)
    
    # Change cells to be all path except for outer ring
    for x in range(1, 10):
        for y in range(1, 10):
            maze.matrix[x][y].is_path = True

    maze.matrix[0][5].is_path = True  # Top is a path too
    maze.matrix[10][5].is_path = True  # Bottom is a path too
    
    # ADD OBJECTS TO A MAZE
    # Add a player to the maze 
    maze.add_entity(Player(maze), 5, 5)  # P

    # Add a warrior to the maze
    maze.add_entity(Warrior(maze), 3, 3)  # W

    # Add a mage to the maze
    maze.add_entity(Mage(maze), 7, 7)  # M

    # Add an archer to the maze
    maze.add_entity(Archer(maze), 3, 7)  # A

    # Add a coin to the maze
    maze.add_entity(Coin(maze), 5, 7)  # C

    # Add a Bomb to the maze
    maze.add_entity(Bomb(maze), 7, 3)  # B

    # Add door at the bottom
    maze.add_entity(Door(maze), 5, 10)  # D

    # Add a key to the maze 
    maze.add_entity(Key(maze), 1, 6)  # K

    # Add an exti to the maze
    maze.add_entity(Exit(maze), 5, 0)  # E

    # Add a trap to the maze
    maze.add_entity(Trap(maze, 5, 9), 5, 2)  # T


    # ==== GAME LOOP ====

    # Find entities in maze by searching for them in the matrix
    maze_entities = update_entity_list(maze)

    # Locate exit
    exit_cell = None
    for entity in maze_entities:
        if isinstance(entity, Exit):
            exit_cell = entity.cell
            break
    if exit_cell is None:
        raise Exception("INVALID MAZE: No exit")
    

    while True:
        # Update the display
        update_display(maze)

        # Movement order:
        # 1. Arrows in maze
        # 2. Player
        # 3. Bomb explosion logic
        # 4. Enemies
        # 5. Archers shoot arrows
        # 6. Mages spawn new bombs

        # Find entities in maze by searching for them in the matrix
        maze_entities = []
        for x in range(maze.width):
            for y in range(maze.height):
                if maze.matrix[x][y].entity is not None:
                    maze_entities.append(maze.matrix[x][y].entity)
        print(f"Entities remaining in maze: {maze_entities}")


        # 1. ARROW MOVING LOGIC
        update_arrows(maze, maze_entities)  # Update arrows in the maze
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        time.sleep(SLEEP_TIME)  # Small delay

        # 2. PLAYER MOVEMENT LOGIC
        win = move_player(maze, maze_entities)
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        if win:
            break
        time.sleep(SLEEP_TIME)  # Small delay

        # 3. BOMB EXPLOSION LOGIC
        update_bombs(maze, maze_entities)
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        time.sleep(SLEEP_TIME)  # Small delay

        # 4. ENEMY MOVEMENT LOGIC
        move_enemies(maze, maze_entities)
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        time.sleep(SLEEP_TIME)  # Small delay
        
        # 5. ARCHER SHOOTING ARROWS LOGIC
        shoot_arrows(maze, maze_entities)
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        time.sleep(SLEEP_TIME)  # Small delay
        
        # 6. MAGE SPAWNING BOMBS LOGIC
        summon_bombs(maze, maze_entities)
        maze_entities = update_entity_list(maze)  # Update the list of entities in the maze in case some were removed
        time.sleep(SLEEP_TIME)  # Small delay
    print("Player escaped!")
    print(f"Total turns to escape: {TURNS_TO_ESCAPE}")
        

if __name__ == "__main__":
    main()