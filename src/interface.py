"""
Module to handle the interface of the game. Both menus and the maze itself.
"""

import pygame
import random
from maze import *
import tkinter as tk
from tkinter import filedialog, messagebox

# Characters
PLAYER_IMG = pygame.image.load("media/sprites/player.png")
ARCHER_IMG = pygame.image.load("media/sprites/archer.png")
WARRIOR_IMG = pygame.image.load("media/sprites/warrior.png")
MAGE_IMG = pygame.image.load("media/sprites/mage.png")

# Static objects
COIN_IMG = pygame.image.load("media/sprites/coin.png")
BOMB_IMG = pygame.image.load("media/sprites/bomb.png")
EXIT_IMG = pygame.image.load("media/sprites/exit.png")
KEY_IMG = pygame.image.load("media/sprites/key.png")
DOOR_IMG = pygame.image.load("media/sprites/door.png")
TRAP_IMG = pygame.image.load("media/sprites/trap.png")

# Tiles
FLOOR_IMG = pygame.image.load("media/sprites/floor.png")
WALL_IMG = pygame.image.load("media/sprites/wall.png")
VOID_IMG = pygame.image.load("media/sprites/void.png")

# Other items
ARROW_IMG = pygame.image.load("media/sprites/arrow.png")
TURNS_IMG = pygame.image.load("media/sprites/turns.png")

# Sfx
pygame.mixer.init()
BOMB_EXPLOSION = pygame.mixer.Sound("media/sfx/explosion.wav")
COIN_PICKUP = pygame.mixer.Sound("media/sfx/coin.wav")
KEY_PICKUP = pygame.mixer.Sound("media/sfx/key.wav")
DOOR_OPEN = pygame.mixer.Sound("media/sfx/door.wav")
TRAP_TRIGGER = pygame.mixer.Sound("media/sfx/teleport.wav")
ARROW_SHOT = pygame.mixer.Sound("media/sfx/shoot.wav")
BOMB_SPAWN = pygame.mixer.Sound("media/sfx/spawn.wav")
PLAYER_MOVE = pygame.mixer.Sound("media/sfx/move.wav")
EXIT_TOUCH = pygame.mixer.Sound("media/sfx/exit.wav")
ARROW_HIT = pygame.mixer.Sound("media/sfx/hit.wav")
ENEMY_KILL = pygame.mixer.Sound("media/sfx/kill.wav")

# Music
GAME_MUSIC = "media/sfx/loop.wav"

# Other constants
VIEW_RANGE = 10  # How many tiles arround the player can be sees (ONLY RENDER THIS VISION SQUARE, FILL REST WITH VOID)
TILE_SIZE = 32  # Size of each tile in pixels
BACKGROUND = (50, 50, 50)  # Color for the background
FONT_FAMILY = "Consolas"  # Font for the text
FONT_SIZE = 24  # Size of the text
FONT_COLOR = (255, 255, 255)  # Color of the text
MINI_SPRITE_SIZE = 64  # Size of the mini sprites in the inventory
INTRO_FINISHED = False  # Flag to check if the intro music has finished playing


def update_display(maze, screen, turns):
    """
    Update the screen with the maze's current state.
    Draw the floor, walls, voids, and objects in two sweeps.
    The player is centered on the screen.
    
    Atributes:
    - maze: Maze object
    - screen: Pygame screen object
    - turns: Number of turns the player has taken
    """

    # Clear the screen
    screen.fill(BACKGROUND)

    # Get the player's position
    player = next(entity for row in maze.matrix for entity in (cell.entity for cell in row) if isinstance(entity, Player))
    player_x, player_y = player.cell.x, player.cell.y

    # Center offsets for drawing
    screen_width, screen_height = screen.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Adjust image sizes to match TILE_SIZE
    scaled_floor = pygame.transform.scale(FLOOR_IMG, (TILE_SIZE, TILE_SIZE))
    scaled_wall = pygame.transform.scale(WALL_IMG, (TILE_SIZE, TILE_SIZE))
    scaled_void = pygame.transform.scale(VOID_IMG, (TILE_SIZE, TILE_SIZE))

    # First sweep: Draw tiles
    for dy in range(-VIEW_RANGE, VIEW_RANGE + 1):
        for dx in range(-VIEW_RANGE, VIEW_RANGE + 1):
            # Real maze coordinates
            maze_x = player_x + dx
            maze_y = player_y + dy

            # Screen coordinates
            screen_x = center_x + dx * TILE_SIZE - TILE_SIZE // 2
            screen_y = center_y + dy * TILE_SIZE - TILE_SIZE // 2

            if 0 <= maze_x < maze.width and 0 <= maze_y < maze.height:
                # Inside maze bounds
                cell = maze.matrix[maze_y][maze_x]
                if cell.is_path:
                    screen.blit(scaled_floor, (screen_x, screen_y))
                else:
                    screen.blit(scaled_wall, (screen_x, screen_y))
            else:
                # Out of bounds; draw void
                screen.blit(scaled_void, (screen_x, screen_y))

    # Second sweep: Draw objects, enemies, arrows, and the player
    for dy in range(-VIEW_RANGE, VIEW_RANGE + 1):
        for dx in range(-VIEW_RANGE, VIEW_RANGE + 1):
            # Real maze coordinates
            maze_x = player_x + dx
            maze_y = player_y + dy

            # Screen coordinates
            screen_x = center_x + dx * TILE_SIZE - TILE_SIZE // 2
            screen_y = center_y + dy * TILE_SIZE - TILE_SIZE // 2

            # Adjust image sizes to match TILE_SIZE
            scaled_coin = pygame.transform.scale(COIN_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_bomb = pygame.transform.scale(BOMB_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_exit = pygame.transform.scale(EXIT_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_key = pygame.transform.scale(KEY_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_door = pygame.transform.scale(DOOR_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_trap = pygame.transform.scale(TRAP_IMG, (TILE_SIZE, TILE_SIZE))

            scaled_player = pygame.transform.scale(PLAYER_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_archer = pygame.transform.scale(ARCHER_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_warrior = pygame.transform.scale(WARRIOR_IMG, (TILE_SIZE, TILE_SIZE))
            scaled_mage = pygame.transform.scale(MAGE_IMG, (TILE_SIZE, TILE_SIZE))

            scaled_arrow = pygame.transform.scale(ARROW_IMG, (TILE_SIZE, TILE_SIZE))

            if 0 <= maze_x < maze.width and 0 <= maze_y < maze.height:
                # Inside maze bounds
                cell = maze.matrix[maze_y][maze_x]
                if cell.entity:
                    entity = cell.entity
                    if isinstance(entity, Coin):
                        screen.blit(scaled_coin, (screen_x, screen_y))
                    elif isinstance(entity, Bomb):
                        screen.blit(scaled_bomb, (screen_x, screen_y))
                    elif isinstance(entity, Exit):
                        screen.blit(scaled_exit, (screen_x, screen_y))
                    elif isinstance(entity, Key):
                        screen.blit(scaled_key, (screen_x, screen_y))
                    elif isinstance(entity, Door):
                        screen.blit(scaled_door, (screen_x, screen_y))
                    elif isinstance(entity, Trap):
                        screen.blit(scaled_trap, (screen_x, screen_y))
                    elif isinstance(entity, Player):
                        screen.blit(scaled_player, (screen_x, screen_y))
                    elif isinstance(entity, Archer):
                        screen.blit(scaled_archer, (screen_x, screen_y))
                    elif isinstance(entity, Warrior):
                        screen.blit(scaled_warrior, (screen_x, screen_y))
                    elif isinstance(entity, Mage):
                        screen.blit(scaled_mage, (screen_x, screen_y))
                    elif isinstance(entity, Arrow):
                        # Rotate image acording to the direction
                        match entity.direction:  # Arrow is drawn to the right by default 
                            case "right":
                                scaled_arrow = pygame.transform.rotate(scaled_arrow, 0)
                            case "left":
                                scaled_arrow = pygame.transform.rotate(scaled_arrow, 180)
                            case "up":
                                scaled_arrow = pygame.transform.rotate(scaled_arrow, 90)
                            case "down":
                                scaled_arrow = pygame.transform.rotate(scaled_arrow, 270)
                            # WARNING: match case requires python 3.10 or newer
                        screen.blit(scaled_arrow, (screen_x, screen_y))

    # Create the font and prepare the images
    font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
    turns_image = pygame.transform.scale(TURNS_IMG, (MINI_SPRITE_SIZE, MINI_SPRITE_SIZE))
    turns_text = font.render(f"Moves x {turns}", True, FONT_COLOR)

    # Positioning the "Moves" icon and text
    turns_x = center_x + VIEW_RANGE * TILE_SIZE + TILE_SIZE // 2 + 10
    turns_y = center_y - TILE_SIZE * 1.5
    turns_text_height = turns_text.get_height()

    # Draw the "Moves" icon and text, centering the text vertically within the mini sprite
    screen.blit(turns_image, (turns_x, turns_y))
    screen.blit(turns_text, (turns_x + MINI_SPRITE_SIZE + 10, turns_y + (MINI_SPRITE_SIZE - turns_text_height) // 2))

    # Get player and keys information
    player = next(entity for row in maze.matrix for entity in (cell.entity for cell in row) if isinstance(entity, Player))
    keys = player.keys
    keys_image = pygame.transform.scale(KEY_IMG, (MINI_SPRITE_SIZE, MINI_SPRITE_SIZE))
    keys_text = font.render(f"Keys x {keys}", True, FONT_COLOR)

    # Positioning the "Keys" icon and text
    keys_x = center_x + VIEW_RANGE * TILE_SIZE + TILE_SIZE // 2 + 10
    keys_y = center_y + TILE_SIZE * 1.5
    keys_text_height = keys_text.get_height()

    # Draw the "Keys" icon and text, centering the text vertically within the mini sprite
    screen.blit(keys_image, (keys_x, keys_y))
    screen.blit(keys_text, (keys_x + MINI_SPRITE_SIZE + 10, keys_y + (MINI_SPRITE_SIZE - keys_text_height) // 2))

    # Update the display
    pygame.display.flip()


def play_sound(sound):
    """
    Play a sound effect.

    Atributes:
    - sound: Name of said sound

    List of available sounds:
    - bomb_explode
    - coin_pickup
    - key_pickup
    - door_open
    - trap_trigger
    - arrow_shot
    - bomb_spawn
    - player_move
    - exit_touch
    - enemy_kill
    - arrow_hit
    """
    sound_library = {   # Dictionary with the sounds and name
        "bomb_explode": BOMB_EXPLOSION,
        "coin_pickup": COIN_PICKUP,
        "key_pickup": KEY_PICKUP,
        "door_open": DOOR_OPEN,
        "trap_trigger": TRAP_TRIGGER,
        "arrow_shot": ARROW_SHOT,
        "bomb_spawn": BOMB_SPAWN,
        "player_move": PLAYER_MOVE,
        "exit_touch": EXIT_TOUCH,
        "enemy_kill": ENEMY_KILL,
        "arrow_hit": ARROW_HIT
    }

    sound_library[sound].play()


def play_music():
    """
    Play the game's music.
    """
    print("Music provided courtesy of Abundant Music (https://pernyblom.github.io/abundant-music/index.html)")
    pygame.mixer.music.load(GAME_MUSIC)
    pygame.mixer.music.play(-1)


def run_menu():
    """
    Runs the menu interface using tkinter.
    Returns:
        str: The path of the selected maze file if any, else an empty string.
        bool: A flag indicating whether to start the game or exit.
    """
    maze_file = ""  # Nonlocal variable to control the maze file (global inside this function only)
    should_run_game = False  # Nonlocal variable to control the menu loop (global inside this function only)

    def on_play():
        nonlocal should_run_game
        if maze_file:
            should_run_game = True  # Signal to start the game
            root.destroy()  # Close the menu window
        else:
            msgbox("No maze loaded", "Please load a maze file before starting the game", 1)

    def on_load_maze():
        nonlocal maze_file
        file_path = filedialog.askopenfilename(title="Select Maze File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            maze_file = file_path
            msgbox("Maze loaded", f"Selected maze file: {maze_file}", 0)
        else:
            msgbox("Invalid file path", "No valid maze file selected", 2)

    def on_exit():
        nonlocal should_run_game
        should_run_game = False  # Signal to exit the game
        root.destroy()

    # Initialize tkinter window
    root = tk.Tk()
    root.title("Maze Game Menu")

    # Create buttons
    play_button = tk.Button(root, text="Play", command=on_play)
    load_button = tk.Button(root, text="Load Maze", command=on_load_maze)
    exit_button = tk.Button(root, text="Exit", command=on_exit)

    # Layout buttons
    play_button.pack(pady=10)
    load_button.pack(pady=10)
    exit_button.pack(pady=10)

    root.mainloop()
    return maze_file, should_run_game


def msgbox(title, message, warning_level):
    """
    Display a message box with a title and a message.

    Atributes:
    - title: Title of the message box
    - message: Message to be displayed
    - warning_level: Level of the message box (0 = info, 1 = warning, 2 = error)
    """
    match warning_level:  # Match the warning level to the corresponding message box
        case 0:
            messagebox.showinfo(title, message)
        case 1:
            messagebox.showwarning(title, message)
        case 2:
            messagebox.showerror(title, message)