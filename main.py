import curses
import os

from game.render import drawMap

os.environ.setdefault("TERM", "xterm-256color")

# 0 = wall
# 1 = floor
MAP = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,0,0,1,1,0],
    [0,1,1,1,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0],
]

HEIGHT = len(MAP)
WIDTH  = len(MAP[0])

def main(stdscr):
    curses.curs_set(0)          # hide cursor
    stdscr.timeout(100)         # non-blocking getch (ms), feels more responsive
    stdscr.keypad(True)         # enable arrow keys too (optional)

    # ─── Colors ───────────────────────────────────────────────
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE,  curses.COLOR_BLACK)   # player
    curses.init_pair(2, curses.COLOR_CYAN,   curses.COLOR_BLACK)   # floor
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # wall (dim)
    curses.init_pair(4, curses.COLOR_BLACK,  curses.COLOR_WHITE)   # player bg (optional)

    player_y, player_x = 2, 2

    while True:
        stdscr.clear()

        # Draw map
        drawMap(MAP, WIDTH, HEIGHT, stdscr)

        # Draw player
        stdscr.addstr(player_y, player_x, "@", curses.color_pair(1) | curses.A_BOLD)

        stdscr.refresh()

        # ─── Input ────────────────────────────────────────────────
        try:
            key = stdscr.getch()
        except:
            key = -1

        new_y, new_x = player_y, player_x

        if key in (ord('q'), 27):           # q or ESC
            break
        
        # Check for VI-KEYS, WASD, and arrow keys

        elif key in (ord('w'), curses.KEY_UP, ord('k')):
            new_y -= 1
        elif key in (ord('s'), curses.KEY_DOWN, ord('j')):
            new_y += 1
        elif key in (ord('a'), curses.KEY_LEFT, ord('h')):
            new_x -= 1
        elif key in (ord('d'), curses.KEY_RIGHT, ord('l')):
            new_x += 1
        elif key == ord(' '):               # wait / rest turn
            pass

        # Collision check
        if 0 <= new_y < HEIGHT and 0 <= new_x < WIDTH:
            if MAP[new_y][new_x] != 0:      # not wall
                player_y, player_x = new_y, new_x

if __name__ == "__main__":
    curses.wrapper(main)