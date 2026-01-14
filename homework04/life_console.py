import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                char = "1" if self.life.curr_generation[row][col] == 1 else "0"
                try:
                    screen.addch(row + 1, col + 1, char)
                except curses.error:
                    pass

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(True)
        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                key = screen.getch()
                if key in (ord("q"), ord("Q")):
                    break
                self.life.step()
        finally:
            curses.endwin()


if __name__ == "__main__":
    life = GameOfLife(size=(20, 40), randomize=True, max_generations=100)
    console = Console(life)
    console.run()
