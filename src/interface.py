"""
Module to handle the interface of the game. Both menus and the maze itself.
"""

import pygame
import random
from maze import *

# Characters
PLAYER_IMG = pygame.image.load("media/player.png")
ARCHER_IMG = pygame.image.load("media/archer.png")
WARRIOR_IMG = pygame.image.load("media/warrior.png")
MAGE_IMG = pygame.image.load("media/mage.png")

# Static objects
COIN_IMG = pygame.image.load("media/coin.png")
BOMB_IMG = pygame.image.load("media/bomb.png")
EXIT_IMG = pygame.image.load("media/exit.png")
KEY_IMG = pygame.image.load("media/key.png")
DOOR_IMG = pygame.image.load("media/door.png")
TRAP_IMG = pygame.image.load("media/trap.png")

# Tiles
FLOOR_IMG = pygame.image.load("media/floor.png")
WALL_IMG = pygame.image.load("media/wall.png")
VOID_IMG = pygame.image.load("media/void.png")

# Other items
ARROW_IMG = pygame.image.load("media/arrow.png")
TURNS_IMG = pygame.image.load("media/turns.png")

# Other constants
VIEW_RANGE = 10  # How many tiles arround the player can be sees (ONLY RENDER THIS VISION SQUARE, FILL REST WITH VOID)
TILE_SIZE = 32  # Size of each tile in pixels
BACKGROUND = (50, 50, 50)  # Color for the background
FONT_FAMILY = "Consolas"  # Font for the text
FONT_SIZE = 24  # Size of the text
FONT_COLOR = (255, 255, 255)  # Color of the text
MINI_SPRITE_SIZE = 64  # Size of the mini sprites in the inventory


def update_display(maze, screen, turns):
    """
    Update the screen with the maze's current state.
    Draw the floor, walls, voids, and objects in two sweeps.
    The player is centered on the screen.
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
