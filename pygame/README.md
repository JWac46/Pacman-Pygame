# Pac-Man Maze Game

A small maze game built with Python and Pygame. Guide the player through the
maze, collect every pellet, and avoid the ghosts.

## Features

- Arrow-key movement through a tile-based maze
- Player sprite rotates to face its movement direction
- Ghosts move around the maze
- Score tracking (10 points per pellet)
- Win and game-over messages

## Requirements

- Python 3
- Pygame
- The player image `pacman-png-25189.png`
- The ghost image `ghost_red.png`

The game loads both image files from the current working directory. Put them
beside `main.py` before starting the game.

## Setup and run

From the directory containing `main.py`, install Pygame if it is not already
installed:

```bash
python -m pip install pygame
```

Then launch the game:

```bash
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| Up arrow | Move up |
| Down arrow | Move down |
| Left arrow | Move left |
| Right arrow | Move right |
| R | Exit after winning or losing |

Close the game window to exit at any time.