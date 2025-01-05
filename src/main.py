import os
import time
import pygame
from maze import *
from interface import *
from parser import parse


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


def update_arrows(maze, maze_entities, screen):
    """
    Update the arrows in the maze, moving them and checking for collisions
    """
    for entity in maze_entities:
        if isinstance(entity, Arrow):
            # Check direction (up, down, left, right)
            match entity.direction:
                case "up":
                    dx = 0
                    dy = -1
                case "down":
                    dx = 0
                    dy = 1
                case "left":
                    dx = -1
                    dy = 0
                case "right":
                    dx = 1
                    dy = 0
                case _:
                    print("Invalid arrow direction")  # Should never happen
            
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
                    play_sound("arrow_hit")
    update_display(maze, screen, TURNS_TO_ESCAPE)

def move_player(maze, maze_entities, screen):
    """
    Wait for player input, process movement, and handle interactions.
    """
    player = None
    moved = False
    win = False
    global TURNS_TO_ESCAPE
    for entity in maze_entities:
        if isinstance(entity, Player):
            player = entity
            break

    while not moved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                match event.key:
                    case pygame.K_w:  # Move up
                        dy = -1
                    case pygame.K_s:  # Move down
                        dy = 1
                    case pygame.K_a:  # Move left
                        dx = -1
                    case pygame.K_d:  # Move right
                        dx = 1
                    case _:
                        print("Invalid key pressed")  # Should never happen

                if dx != 0 or dy != 0:
                    if maze.move_entity(player, dx, dy):
                        moved = True
                        TURNS_TO_ESCAPE += 1
                        play_sound("player_move")
                    else:
                        # Collision and interaction logic
                        target_cell_x = player.cell.x + dx
                        target_cell_y = player.cell.y + dy

                        if 0 <= target_cell_x < maze.width and 0 <= target_cell_y < maze.height:
                            target_cell = maze.matrix[target_cell_y][target_cell_x]
                        else:
                            print("Error moving player: Out of bounds")
                            update_display(maze, screen, TURNS_TO_ESCAPE)
                            break
                        
                        # Check if it failed due to hitting the exit
                        if target_cell.entity is not None and isinstance(target_cell.entity, Exit):
                            TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                            target_cell.entity = None  # Remove the exit from the maze
                            maze.move_entity(player, dx, dy)  # Redo the move
                            play_sound("exit_touch")
                            moved = True
                            update_display(maze, screen, TURNS_TO_ESCAPE)
                            win = True
                            break
                            
                        # Check if it failed due to hitting a coin
                        if target_cell.entity is not None and isinstance(target_cell.entity, Coin):
                            TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                            TURNS_TO_ESCAPE -= 3  # Reduce turn count by 3 (value of coin)
                            if TURNS_TO_ESCAPE < 0:
                                TURNS_TO_ESCAPE = 0
                            target_cell.entity = None  # Remove the coin from the maze
                            maze.move_entity(player, dx, dy) # Redo the move
                            play_sound("coin_pickup")
                            moved = True
                            update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting a key
                        if target_cell.entity is not None and isinstance(target_cell.entity, Key):
                            TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                            player.keys += 1  # Give the player a key
                            target_cell.entity = None  # Remove the key from the maze
                            maze.move_entity(player, dx, dy) # Redo the move
                            play_sound("key_pickup")
                            moved = True
                            update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting a door
                        if target_cell.entity is not None and isinstance(target_cell.entity, Door):
                            # Check if we have a key
                            if player.keys > 0:
                                player.keys -= 1  # Use a key
                                TURNS_TO_ESCAPE += 1 # Increment the turn count because move is valid
                                target_cell.entity = None  # Remove the door from the maze
                                maze.move_entity(player, dx, dy) # Redo the move
                                play_sound("door_open")
                                moved = True
                                update_display(maze, screen, TURNS_TO_ESCAPE)
                            else:
                                print("Player hit a door without a key")
                                update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting a trap
                        if target_cell.entity is not None and isinstance(target_cell.entity, Trap):
                            if maze.teleport_entity(player, target_cell.entity.target_x, target_cell.entity.target_y):
                                print("Player hit a trap and teleported")
                                TURNS_TO_ESCAPE += 1  # Increment the turn count because move is valid
                                play_sound("trap_trigger")
                                moved = True
                                update_display(maze, screen, TURNS_TO_ESCAPE)
                            else:  # Target is blocked
                                print("Player hit a trap but couldn't teleport. Exit blocked by something")
                                update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting a warrior
                        if target_cell.entity is not None and isinstance(target_cell.entity, Warrior):
                            print("Warrior collision")
                            target_cell.entity = None  # Kill enemy
                            TURNS_TO_ESCAPE += 2  # 2 turns, one for the move, one because it was a warrior
                            print("Player hit a warrior and killed it")
                            play_sound("enemy_kill")
                            moved = True
                            update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting an archer or mage
                        if target_cell.entity is not None and (isinstance(target_cell.entity, Archer) or isinstance(target_cell.entity, Mage)):
                            print("Player hit an archer or mage")
                            target_cell.entity = None  # Kill enemy
                            TURNS_TO_ESCAPE += 1
                            maze.move_entity(player, dx, dy)  # Redo the move
                            play_sound("enemy_kill")
                            moved = True
                            update_display(maze, screen, TURNS_TO_ESCAPE)


                        # Check if it failed due to hitting an arrow
                        if target_cell.entity is not None and isinstance(target_cell.entity, Arrow):
                            target_cell.entity = None  # Tank the arrow but don't move, wasting a turn
                            TURNS_TO_ESCAPE += 1
                            play_sound("arrow_hit")
                            moved = True
                            print("Player hit an arrow and tanked it")
                            update_display(maze, screen, TURNS_TO_ESCAPE)

                        # Check if it failed due to hitting a bomb
                        if target_cell.entity is not None and isinstance(target_cell.entity, Bomb):
                            update_bombs(maze, maze_entities, screen)
                            update_display(maze, screen, TURNS_TO_ESCAPE)
                            moved = True

    # Update arrows to allow movement after player completes turn
    for entity in maze_entities:
        if isinstance(entity, Arrow):
            entity.can_move = True
    update_display(maze, screen, TURNS_TO_ESCAPE)
    return win


def update_bombs(maze, maze_entities, screen):
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
                    play_sound("bomb_explode")
                    print("Bomb hit player and exploded")
    update_display(maze, screen, TURNS_TO_ESCAPE)


def move_enemies(maze, maze_entities, screen):
    """
    Move the enemies in the maze randomly
    """
    for entity in maze_entities:  # Locate all enemies
        if isinstance(entity, Warrior) or isinstance(entity, Archer) or isinstance(entity, Mage):
            direction = random.choice(["up", "down", "left", "right"])
            move_chance = random.randint(1, 5)  # 1/5 chance to move
            if move_chance == 1:
                match direction:
                    case "up":
                        dx = 0
                        dy = -1
                    case "down":
                        dx = 0
                        dy = 1
                    case "left":
                        dx = -1
                        dy = 0
                    case "right":
                        dx = 1
                        dy = 0
                    case _:
                        print("Invalid direction")  # Should never happen
                if not maze.move_entity(entity, dx, dy):
                    print(f"{entity} failed to move to {dx}, {dy}")
    update_display(maze, screen, TURNS_TO_ESCAPE)


def shoot_arrows(maze, maze_entities, screen):
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
                else:
                    play_sound("arrow_shot")
                update_display(maze, screen, TURNS_TO_ESCAPE) 


def summon_bombs(maze, maze_entities, screen):
    """
    Create new bombs from mages
    """
    for entity in maze_entities:
        if isinstance(entity, Mage):
            # Decide if the mage will spawn a bomb (1/10 chance)
            if random.randint(1, 10) == 1:
                if entity.spawn_bomb():
                    play_sound("bomb_spawn")
                update_display(maze, screen, TURNS_TO_ESCAPE)


def build_maze(file_path):
    """
    Build a maze from a file
    """
    maze = None
    with open(file_path, 'r') as file:  # Read the file content
        input_string = file.read()
    
    print(f"Building maze from: {file_path}\n")

    print("\nParser output:")
    try:
        maze = parse(input_string)  # Parse the input using the parser
        print("Parsing successful!")
    except Exception as e:
        print(f"Parsing failed: {e}")
    return maze


TURNS_TO_ESCAPE = 0  # Number of turns used to escape the maze (global variable)
def main():

    maze_file = "./Maze/ej_maze_correcto_semantica.txt"
    if not os.path.exists(maze_file):
        print(f"File not found: {maze_file}")

    # Build the maze from the file
    maze = build_maze(maze_file)
    if maze is None:
        print("Maze not created")
        # Create alternate test maze

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

        # Add an exit to the maze
        maze.add_entity(Exit(maze), 5, 0)  # E

        # Add a trap to the maze
        maze.add_entity(Trap(maze, 5, 9), 5, 2)  # T (target first, then location)

    # ==== GAME LOOP ====
    # Create pygame window (adjust to window size)
    pygame.init()
    icon_img = pygame.image.load("media/sprites/icon.png")
    pygame.display.set_icon(icon_img)  # Add this line
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("SQUID GAMES❗❗")
    clock = pygame.time.Clock()
    play_music()
    
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
    
    running = True
    while running:
        # Event handling for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the display (can show the current state of the maze)
        update_display(maze, screen, TURNS_TO_ESCAPE)

        # 1. Player Movement (waits for input)
        win = move_player(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)  # Refresh entity list after player's move
        if win:  # If the player wins, exit the loop
            break

        # 2. Arrow Movement
        update_arrows(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)

        # 3. Bomb Explosion Logic
        update_bombs(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)

        # 4. Enemy Movement Logic
        move_enemies(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)

        # 5. Archers Shoot Arrows
        shoot_arrows(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)

        # 6. Mages Spawn Bombs
        summon_bombs(maze, maze_entities, screen)
        maze_entities = update_entity_list(maze)

        # Update the display again at the end of the turn
        update_display(maze, screen, TURNS_TO_ESCAPE)
        clock.tick(30)  # Limit to 30 FPS

    print("Player escaped!")
    print(f"Total turns to escape: {TURNS_TO_ESCAPE}")
        

if __name__ == "__main__":
    main()
    time.sleep(1)