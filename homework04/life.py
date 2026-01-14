import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = []
        for row in range(self.rows):
            grid_row: Cells = []
            for col in range(self.cols):
                cell_value = random.randint(0, 1) if randomize else 0
                grid_row.append(cell_value)
            grid.append(grid_row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours: Cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbour_row = row + i
                neighbour_col = col + j
                if 0 <= neighbour_row < self.rows and 0 <= neighbour_col < self.cols:
                    neighbours.append(self.curr_generation[neighbour_row][neighbour_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid: Grid = []
        for row in range(self.rows):
            new_row: Cells = []
            for col in range(self.cols):
                current_cell = self.curr_generation[row][col]
                alive_neighbours = sum(self.get_neighbours((row, col)))
                if current_cell == 1:
                    new_row.append(1 if alive_neighbours in (2, 3) else 0)
                else:
                    new_row.append(1 if alive_neighbours == 3 else 0)
            new_grid.append(new_row)
        return new_grid

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
            rows = len(lines)
            cols = len(lines[0]) if rows > 0 else 0
            game = GameOfLife((rows, cols), randomize=False, max_generations=None)
            for i, line in enumerate(lines):
                for j, char in enumerate(line):
                    game.curr_generation[i][j] = 1 if char == "1" else 0
            return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join(str(cell) for cell in row) + "\n")
