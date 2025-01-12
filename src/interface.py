"""
Module to handle the interface of the game. Both the menu and the maze itself.
"""

import pygame
import random
from maze import *
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage

# Characters
PLAYER_IMG = pygame.image.load("media/sprites/player.png")  # Player sprite
ARCHER_IMG = pygame.image.load("media/sprites/archer.png")  # Archer sprite
WARRIOR_IMG = pygame.image.load("media/sprites/warrior.png")  # Warrior sprite
MAGE_IMG = pygame.image.load("media/sprites/mage.png")  # Mage sprite

# Static objects
COIN_IMG = pygame.image.load("media/sprites/coin.png")  # Coin sprite
BOMB_IMG = pygame.image.load("media/sprites/bomb.png")  # Bomb sprite
EXIT_IMG = pygame.image.load("media/sprites/exit.png")  # Exit sprite
KEY_IMG = pygame.image.load("media/sprites/key.png")  # Key sprite
DOOR_IMG = pygame.image.load("media/sprites/door.png")  # Door sprite
TRAP_IMG = pygame.image.load("media/sprites/trap.png")  # Trap sprite

# Tiles
FLOOR_IMG = pygame.image.load("media/sprites/floor.png")  # Floor sprite
WALL_IMG = pygame.image.load("media/sprites/wall.png")  # Wall sprite
VOID_IMG = pygame.image.load("media/sprites/void.png")  # Void sprite (out of bounds)

# Other items
ARROW_IMG = pygame.image.load("media/sprites/arrow.png")  # Arrow sprite
TURNS_IMG = pygame.image.load("media/sprites/turns.png")  # "Moves" icon

# MENU ICONS
PLAY_ICON = "media/sprites/play_icon.png"  # Play button icon
LOAD_ICON = "media/sprites/load_icon.png"  # Load button icon
EXIT_ICON = "media/sprites/exit_icon.png"  # Exit button icon
HELP_ICON = "media/sprites/help_icon.png"  # Help button icon

# Sfx
pygame.mixer.init()
pygame.mixer.set_num_channels(64)  # Increase the number of channels to avoid cutting off sounds (64 is overkill but just in case)
BOMB_EXPLOSION = pygame.mixer.Sound("media/sfx/explosion.wav")  # Sound for the bomb explosion
COIN_PICKUP = pygame.mixer.Sound("media/sfx/coin.wav")  # Sound for the coin pickup
KEY_PICKUP = pygame.mixer.Sound("media/sfx/key.wav")  # Sound for the key pickup
DOOR_OPEN = pygame.mixer.Sound("media/sfx/door.wav")  # Sound for the door opening
TRAP_TRIGGER = pygame.mixer.Sound("media/sfx/teleport.wav")  # Sound for the trap trigger
ARROW_SHOT = pygame.mixer.Sound("media/sfx/shoot.wav")  # Sound for the arrow shot
BOMB_SPAWN = pygame.mixer.Sound("media/sfx/spawn.wav")  # Sound for the bomb spawn
PLAYER_MOVE = pygame.mixer.Sound("media/sfx/move.wav")  # Sound for the player moving
EXIT_TOUCH = pygame.mixer.Sound("media/sfx/exit.wav")  # Sound for the player touching the exit
ARROW_HIT = pygame.mixer.Sound("media/sfx/hit.wav")  # Sound for the arrow hitting an enemy
ENEMY_KILL = pygame.mixer.Sound("media/sfx/kill.wav")  # Sound for an enemy being killed

# Music
GAME_MUSIC = "media/sfx/loop.wav"

# Menu colors
MENU_BG = (50, 50, 50)  # Background color for the menu
MENU_FG_COLOR = (255, 255, 255)  # Foreground color for the menu
BUTTON_COLOR = (120, 120, 120)  # Color for the buttons
BUTTON_ACTIVE_COLOR = (155, 155, 155)  # Color for the buttons when pressed
TEXTBOX_BG = (170, 170, 170)  # Background color for the text box
MENU_FONT_COLOR = (5, 5, 5)  # Font color for the menu

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

            if 0 <= maze_x < maze.width and 0 <= maze_y < maze.height:  # Inside maze bounds
                cell = maze.matrix[maze_y][maze_x]
                if cell.entity:
                    entity = cell.entity
                    match entity:  # Match the entity to the corresponding sprite
                        case Coin():
                            screen.blit(scaled_coin, (screen_x, screen_y))
                        case Bomb():
                            screen.blit(scaled_bomb, (screen_x, screen_y))
                        case Exit():
                            screen.blit(scaled_exit, (screen_x, screen_y))
                        case Key():
                            screen.blit(scaled_key, (screen_x, screen_y))
                        case Door():
                            screen.blit(scaled_door, (screen_x, screen_y))
                        case Trap():
                            screen.blit(scaled_trap, (screen_x, screen_y))
                        case Player():
                            screen.blit(scaled_player, (screen_x, screen_y))
                        case Archer():
                            screen.blit(scaled_archer, (screen_x, screen_y))
                        case Warrior():
                            screen.blit(scaled_warrior, (screen_x, screen_y))
                        case Mage():
                            screen.blit(scaled_mage, (screen_x, screen_y))
                        case Arrow():
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
                            screen.blit(scaled_arrow, (screen_x, screen_y))
                        case _:
                            raise ValueError(f"Unknown entity: {entity}")
                    

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
    pygame.mixer.music.set_volume(0.2)  # Lower volume (20%) because it can get quite loud with headphones
    pygame.mixer.music.play(-1)


def show_menu():
    """
    Runs the menu interface using tkinter.
    Returns:
        str: The path of the selected maze file if any, else an empty string.
        bool: A flag indicating whether to start the game or exit.
    """
    maze_file = ""  # Nonlocal variable to control the maze file (global inside this function only)
    should_run_game = False  # Nonlocal variable to control the menu loop (global inside this function only)
    icon = "media/sprites/icon.png"  # Icon for the window

    def on_play():  # Callback for the play button
        nonlocal should_run_game
        play_sound("arrow_hit")
        if maze_file:
            should_run_game = True  # Signal to start the game
            root.destroy()  # Close the menu window
        else:
            msgbox("No maze loaded", "Please load a maze file before starting the game", 1)

    def on_load_maze():  # Callback for the load maze button
        nonlocal maze_file
        play_sound("arrow_hit")
        file_path = filedialog.askopenfilename(title="Select Maze File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            maze_file = file_path
            textbox_text = maze_file.split("/")[-1]  # Get the file name only
            textbox.config(state=tk.NORMAL)  # Enable editing
            textbox.delete("1.0", tk.END)  # Clear the textbox
            textbox.insert(tk.END, textbox_text, "center")  # Write the file name
            textbox.config(state=tk.DISABLED)  # Disable editing
        else:
            msgbox("Invalid file path", "No valid maze file selected", 2)

    def on_exit():  # Callback for the exit button
        nonlocal should_run_game
        play_sound("arrow_hit")
        should_run_game = False  # Signal to exit the game
        root.destroy()

    def on_help():  # Callback for the help button
        play_sound("arrow_hit")
        line_1 = "- Use WASD or the arrow keys to move the arround the maze."
        line_2 = "- Doors can be opened with keys, and traps can be triggered by stepping on them to teleport."
        line_3 = "- The objective is to reach the exit portal with the least amount of moves possible."
        line_4 = "- Collecting coins will reduce the moves taken, while stepping near bombs will increase them."
        line_5 = "- Archers shoot arrows that push entities"
        line_6 = "- Mages spawn up to 5 bombs randomly arround the maze"
        line_7 = "- Warriors move randomly arround the maze but taking them down costs more moves"
        msgbox("Help", f"{line_1}\n\n{line_2}\n\n{line_3}\n\n{line_4}\n\n{line_5}\n\n{line_6}\n\n{line_7}", 0)


    # Initialize tkinter window
    root = tk.Tk()
    root.title("Dungeon Escape Menu")
    root.resizable(False, False)
    root.geometry("575x500")
    root.iconphoto(False, tk.PhotoImage(file=icon))
    root.config(bg=rgb_to_hex(MENU_BG))
    menu_font = (FONT_FAMILY, FONT_SIZE, "bold")  # Font for the menu buttons
    textbox_font = (FONT_FAMILY, int(FONT_SIZE / 2))  # Smaller font for the textbox (half the size)
    title_font = (FONT_FAMILY, int(FONT_SIZE * 2), "bold")  # Bigger font for the title (twice the size)
    play_icon = PhotoImage(file=PLAY_ICON)
    load_icon = PhotoImage(file=LOAD_ICON)
    exit_icon = PhotoImage(file=EXIT_ICON)
    help_icon = PhotoImage(file=HELP_ICON)
    wall_texture = "media/sprites/wall.png"

    # Create a tiled background
    canvas = tk.Canvas(root, width=1000, height=1000)  # Bigger than the window so it doesn't align on any edge
    canvas.place(relwidth=1, relheight=1)
    texture = PhotoImage(file=wall_texture)
    for x in range(0, 1000, texture.width()):  # Bigger than the window so it doesn't align on any edge
        for y in range(0, 1000, texture.height()):  
            canvas.create_image(x, y, image=texture, anchor="center")

    # Create buttons
    play_button = tk.Button(root, text="Play", command=on_play, font=menu_font, image=play_icon, width=225, height=50, compound="left", padx=10)
    play_button.config(bg=rgb_to_hex(BUTTON_COLOR), activebackground=rgb_to_hex(BUTTON_ACTIVE_COLOR), fg=rgb_to_hex(MENU_FONT_COLOR))
    load_button = tk.Button(root, text="Load Maze", command=on_load_maze, font=menu_font, image=load_icon, width=225, height=50, compound="left", padx=10)
    load_button.config(bg=rgb_to_hex(BUTTON_COLOR), activebackground=rgb_to_hex(BUTTON_ACTIVE_COLOR), fg=rgb_to_hex(MENU_FONT_COLOR))
    exit_button = tk.Button(root, text="Exit", command=on_exit, font=menu_font, image=exit_icon, width=225, height=50, compound="left", padx=10)
    exit_button.config(bg=rgb_to_hex(BUTTON_COLOR), activebackground=rgb_to_hex(BUTTON_ACTIVE_COLOR), fg=rgb_to_hex(MENU_FONT_COLOR))
    help_button = tk.Button(root, text="Help", command=on_help, font=menu_font, image=help_icon, width=225, height=50, compound="left", padx=10)
    help_button.config(bg=rgb_to_hex(BUTTON_COLOR), activebackground=rgb_to_hex(BUTTON_ACTIVE_COLOR), fg=rgb_to_hex(MENU_FONT_COLOR))

    # Create textbox
    textbox = tk.Text(root, height=1, width=45)
    textbox.insert(tk.END, maze_file)
    textbox.tag_configure("center", justify="center")  # Tag to center text
    textbox.config(state=tk.DISABLED, bg=rgb_to_hex(TEXTBOX_BG), font=textbox_font, fg=rgb_to_hex(MENU_FONT_COLOR), borderwidth=3, relief="sunken")

    # Create label
    title_label = tk.Label(root, text="Dungeon Escape", font=title_font, fg=rgb_to_hex(MENU_FONT_COLOR), bg=rgb_to_hex(TEXTBOX_BG), padx=20, borderwidth=3, relief="sunken")

    # Layout elements
    title_label.pack(pady=20)
    play_button.pack(pady=10)
    load_button.pack(pady=10)
    textbox.pack(pady=10)
    help_button.pack(pady=10)
    exit_button.pack(pady=10)

    # Play a sound when the window is opened
    play_sound("exit_touch")

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


def rgb_to_hex(rgb):
    """
    Convert an RGB tuple to a hex color string.ç

    Atributes:
    - rgb: Tuple with the RGB values (int, int, int)
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
