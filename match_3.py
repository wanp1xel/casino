import pygame
import random
import sys
import time

pygame.init()

screen_width = 1500
screen_height = 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Match-3 Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECT_COLOR = (255, 255, 255)

# Load images
cherry = pygame.image.load('img/match3/cherry.png')
kivi = pygame.image.load('img/match3/kivi.png')
lemon = pygame.image.load('img/match3/lemon.png')
melon = pygame.image.load('img/match3/melon.png')

# Load background image and scale it
background = pygame.image.load('img/match3/match3.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Scale images to tile size
TILE_SIZE = 70  # Updated tile size
TEXT_SIZE = 65
cherry = pygame.transform.scale(cherry, (TEXT_SIZE, TEXT_SIZE))
kivi = pygame.transform.scale(kivi, (TEXT_SIZE, TEXT_SIZE))
lemon = pygame.transform.scale(lemon, (TEXT_SIZE, TEXT_SIZE))
melon = pygame.transform.scale(melon, (TEXT_SIZE, TEXT_SIZE))

# List of images
FRUITS = [cherry, kivi, lemon, melon]

GRID_SIZE = 8

def create_grid():
    grid = []
    for row in range(GRID_SIZE):
        grid.append([])
        for col in range(GRID_SIZE):
            fruit = random.choice(FRUITS)
            grid[row].append(fruit)

            # Ensure no initial matches
            if col >= 2 and grid[row][col] == grid[row][col - 1] == grid[row][col - 2]:
                while grid[row][col] == grid[row][col - 1]:
                    grid[row][col] = random.choice(FRUITS)

            if row >= 2 and grid[row][col] == grid[row - 1][col] == grid[row - 2][col]:
                while grid[row][col] == grid[row - 1][col]:
                    grid[row][col] = random.choice(FRUITS)
    return grid

def draw_background():
    screen.blit(background, (0, 0))

def draw_grid(grid, selected_tile=None):
    start_x = (screen_width - (GRID_SIZE * TILE_SIZE)) // 2
    start_y = ((screen_height - (GRID_SIZE * TILE_SIZE)) // 2) + 30

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is not None:
                screen.blit(grid[row][col], (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE))
                # pygame.draw.rect(screen, WHITE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    
    if selected_tile:
        row, col = selected_tile
        pygame.draw.rect(screen, SELECT_COLOR, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)

def check_matches(grid, initial=False):
    matched = []
    
    for row in range(len(grid)):
        for col in range(len(grid[row]) - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2] and grid[row][col] is not None:
                matched.extend([(row, col), (row, col + 1), (row, col + 2)])
    
    for col in range(len(grid[0])):
        for row in range(len(grid) - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] and grid[row][col] is not None:
                matched.extend([(row, col), (row + 1, col), (row + 2, col)])
    
    if initial and matched:
        return True
    return matched

def swap_tiles(grid, pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    grid[row1][col1], grid[row2][col2] = grid[row2][col2], grid[row1][col1]

def remove_matches(grid, matches):
    for row, col in matches:
        grid[row][col] = None  

def drop_tiles(grid):
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] is None:
                for upper_row in range(row - 1, -1, -1):
                    if grid[upper_row][col] is not None:
                        grid[row][col] = grid[upper_row][col]
                        grid[upper_row][col] = None
                        break

def refill_grid(grid):
    new_blocks = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is None:
                grid[row][col] = random.choice(FRUITS)
                new_blocks.append((row, col))
    return new_blocks



def animate_swap(grid, pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    start_x = (screen_width - (GRID_SIZE * TILE_SIZE)) // 2
    start_y = ((screen_height - (GRID_SIZE * TILE_SIZE)) // 2) + 30
    
    x1, y1 = start_x + col1 * TILE_SIZE, start_y + row1 * TILE_SIZE
    x2, y2 = start_x + col2 * TILE_SIZE, start_y + row2 * TILE_SIZE
    
    dx, dy = (x2 - x1) // 10, (y2 - y1) // 10
    
    for i in range(10):
        draw_background()
        draw_grid(grid)
        screen.blit(grid[row1][col1], (x1 + dx * i, y1 + dy * i))
        screen.blit(grid[row2][col2], (x2 - dx * i, y2 - dy * i))
        pygame.display.update()
        pygame.time.delay(30)

    swap_tiles(grid, pos1, pos2)

def are_adjacent(pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    return abs(row1 - row2) + abs(col1 - col2) == 1

def match_3_game(screen_width,screen_height):
    grid = create_grid()
    selected_tile = None
    running = True
    clock = pygame.time.Clock()  

    while running:
        draw_background()
        draw_grid(grid, selected_tile)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                start_x = (screen_width - (GRID_SIZE * TILE_SIZE)) // 2
                start_y = ((screen_height - (GRID_SIZE * TILE_SIZE)) // 2) + 30
                col = (mouse_x - start_x) // TILE_SIZE
                row = (mouse_y - start_y) // TILE_SIZE

                # Check if the click is within the grid area
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if selected_tile:
                        if are_adjacent(selected_tile, (row, col)) and grid[selected_tile[0]][selected_tile[1]] != grid[row][col]:
                            animate_swap(grid, selected_tile, (row, col))
                            matches = check_matches(grid)
                            if matches:
                                while matches:
                                    remove_matches(grid, matches)
                                    drop_tiles(grid)
                                    new_blocks = refill_grid(grid)
                                    matches = check_matches(grid)
                            else:
                                animate_swap(grid, (row, col), selected_tile)
                        selected_tile = None
                    else:
                        selected_tile = (row, col)

        pygame.display.update()
        clock.tick(60)  

    pygame.quit()  

if __name__ == "__main__":
    match_3_game()
