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
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)  # 50% шанс быть живой
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j

                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbours.append(self.curr_generation[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(randomize=False)

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)

                if self.curr_generation[i][j] == 1:
                    if alive_neighbours == 2 or alive_neighbours == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if alive_neighbours == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations == None:
            raise ValueError("There is no max generations value")
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        rows: list[list[int]] = []
        with open(filename, "r") as inp:
            for line in inp:
                rows.append(list(map(int, line.strip().split())))
        row_count, col_count = len(rows), len(rows[0])
        output = GameOfLife((row_count, col_count), False)
        output.curr_generation = rows
        return output

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as out:
            current_state = self.curr_generation
            for row in current_state:
                out.write(" ".join(map(str, row)) + "\n")
