import curses

# Draw the map into the screen
def drawMap(MAP, WIDTH, HEIGHT, stdscr):
    """Draw the MAP defines in defines.py into the screen"""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if MAP[y][x] == 0:
                stdscr.addch(y, x, '#', curses.color_pair(3))
            else:
                stdscr.addch(y, x, '.', curses.color_pair(2) | curses.A_DIM)