import curses
from collections import deque
from datetime import datetime
from typing import Optional

class Logger:
    """
    Simple scrolling message logger for curses-based roguelikes.
    Messages appear at the bottom and scroll upward when the buffer is full.
    """

    def __init__(
        self,
        window: curses.window,
        max_lines: int = 5,
        timestamp: bool = False,
        wrap: bool = True
    ):
        self.window = window
        self.max_lines = max_lines
        self.use_timestamp = timestamp
        self.wrap = wrap

        # Message buffer (newest messages at the end)
        self.messages: deque[tuple[str, int]] = deque(maxlen=max_lines)  # (text, attr)

        # Default colors/attributes
        self._init_colors()

        # Initial draw
        self._redraw()

    def _init_colors(self):
        # Pair numbers 1–8 are reserved for game → we start from 10
        curses.init_pair(10, curses.COLOR_WHITE,   curses.COLOR_BLACK)   # normal / info
        curses.init_pair(11, curses.COLOR_YELLOW,  curses.COLOR_BLACK)   # warn / important
        curses.init_pair(12, curses.COLOR_RED,     curses.COLOR_BLACK)   # error / damage
        curses.init_pair(13, curses.COLOR_CYAN,    curses.COLOR_BLACK)   # player actions
        curses.init_pair(14, curses.COLOR_GREEN,   curses.COLOR_BLACK)   # heal / gain
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # rare / magic

        self.DEFAULT  = curses.color_pair(10)
        self.WARN     = curses.color_pair(11) | curses.A_BOLD
        self.ERROR    = curses.color_pair(12) | curses.A_BOLD
        self.PLAYER   = curses.color_pair(13) | curses.A_BOLD
        self.GOOD     = curses.color_pair(14) | curses.A_BOLD
        self.RARE     = curses.color_pair(15) | curses.A_BOLD

    def _redraw(self):
        self.window.clear()
        h, w = self.window.getmaxyx()

        # Show newest messages at the bottom
        for i, (msg, attr) in enumerate(self.messages):
            y = h - len(self.messages) + i
            if y >= h:
                continue

            # Optional timestamp
            prefix = ""
            if self.use_timestamp:
                now = datetime.now().strftime("%H:%M:%S ")
                prefix = now

            line = prefix + msg

            # Truncate or wrap
            if len(line) >= w - 2:
                if self.wrap:
                    line = line[:w-5] + "..."
                else:
                    line = line[:w-2]

            try:
                self.window.addstr(y, 1, line, attr)
            except curses.error:
                pass  # edge case when window too small

        self.window.refresh()

    # ── Public logging methods ───────────────────────────────────────

    def msg(self, text: str, attr: Optional[int] = None):
        """Generic message with custom attribute"""
        self.messages.append((text, attr or self.DEFAULT))
        self._redraw()

    def info(self, text: str):
        """Normal gameplay information"""
        self.msg(text, self.DEFAULT)

    def warn(self, text: str):
        """Something important / suspicious"""
        self.msg(text, self.WARN)

    def error(self, text: str):
        """Critical error or very bad event"""
        self.msg(text, self.ERROR)

    def player(self, text: str):
        """Actions the player character performs"""
        self.msg(text, self.PLAYER)

    def good(self, text: str):
        """Healing, gaining xp, finding good items..."""
        self.msg(text, self.GOOD)

    def combat(self, text: str):
        """Damage / attack messages (red)"""
        self.msg(text, self.ERROR)

    def rare(self, text: str):
        """Rare events, powerful items, magic effects..."""
        self.msg(text, self.RARE)

    def clear(self):
        """Clear all messages"""
        self.messages.clear()
        self._redraw()

    def add_line(self, text: str, attr: Optional[int] = None):
        """Alias for msg()"""
        self.msg(text, attr)