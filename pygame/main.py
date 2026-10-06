from tkinter import font

import pygame
import random

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Window")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
try:
    PACMAN = pygame.image.load("pacman-png-25189.png")
    GHOST = pygame.image.load("ghost_red.png")
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()


maze = [
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    
]

TILE_SIZE = 40
ROWS = len(maze)
COLS = len(maze[0])

PACMAN = pygame.transform.scale(PACMAN, (TILE_SIZE, TILE_SIZE))
GHOST = pygame.transform.scale(GHOST, (TILE_SIZE, TILE_SIZE))

player_x, player_y = 1, 1
player_dir = (0, 0)
next_dir = (0, 0)

ghosts = [[19, 12], [19, 11]]
ghost_dirs = [(0, 0), (0, 0)]

score = 0
font = pygame.font.Font(None, 36)
game_over = False
won = False


def can_move(x, y):
    if 0 <= x < COLS and 0 <= y < ROWS:
        return maze[y][x] != 1
    return False

def rotate_image(image, direction):
    if direction == (0, -1):
        return pygame.transform.rotate(image, -90)
    elif direction == (0, 1):
        return pygame.transform.rotate(image, 90)
    elif direction == (-1, 0):
        return pygame.transform.rotate(image, 0)
    elif direction == (1, 0):
        return pygame.transform.rotate(image, 180)
    return image

def turn_ghost(image, direction):
    if direction == (-1, 0):
        return pygame.transform.flip(image, True, False)
    return image

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                next_dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                next_dir = (0, 1)
            elif event.key == pygame.K_LEFT:
                next_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                next_dir = (1, 0)
            elif event.key == pygame.K_r and (game_over or won):
                running = False
    if not game_over and not won:
        # Move Player
        if can_move(player_x + next_dir[0], player_y + next_dir[1]):
            player_dir = next_dir

        new_x = player_x + player_dir[0]
        new_y = player_y + player_dir[1]

        if can_move(new_x, new_y):
            player_x = new_x
            player_y = new_y

        if maze[player_y][player_x] == 0:
            maze[player_y][player_x] = 2
            score += 10

        pellets_left = sum(row.count(0) for row in maze)
        if pellets_left == 0:
            won = True

        for i, (gx, gy) in enumerate(ghosts):
            dx, dy = ghost_dirs[i]

            next_gx, next_gy = gx + dx, gy + dy
            if not can_move(next_gx, next_gy):
                possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                random.shuffle(possible_dirs)
                for pdx, pdy in possible_dirs:
                    if can_move(gx + pdx, gy + pdy):
                        ghost_dirs[i] = (pdx, pdy)
                        break
            else:
                if random.random() < 0.1:
                    possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    valid_dirs = []
                    for pdx, pdy in possible_dirs:
                        if can_move(gx + pdx, gy + pdy):
                            valid_dirs.append((pdx, pdy))
                    if valid_dirs:
                        ghost_dirs[i] = random.choice(valid_dirs)
                ghosts[i][0] += ghost_dirs[i][0]
                ghosts[i][1] += ghost_dirs[i][1]

            if player_x == ghosts[i][0] and player_y == ghosts[i][1]:
                game_over = True

    screen.fill(BLACK)
    
    # Draw Maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif cell == 0:
                # Pellet
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
    
    #Player         
    player_image = rotate_image(PACMAN, player_dir)
    screen.blit(player_image, (player_x * TILE_SIZE, player_y * TILE_SIZE))
    
    
    # Ghosts
    for i, (gx, gy) in enumerate(ghosts):
        ghost_image = turn_ghost(GHOST, ghost_dirs[i])
        screen.blit(ghost_image, (gx * TILE_SIZE, gy * TILE_SIZE))
    # for gx, gy in ghosts:
    #     screen.blit(GHOST, (gx * TILE_SIZE, gy * TILE_SIZE))
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - game_over_text.get_height() // 2))
    elif won:
        win_text = font.render("You Win!", True, WHITE)
        screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 2 - win_text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(8)

pygame.quit()