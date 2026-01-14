import random
from copy import deepcopy
from typing import List, Optional, Tuple, Union

import pandas as pd

Cell = Union[str, int]


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Cell]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Cell]], coord: Tuple[int, int]) -> List[List[Cell]]:
    x, y = coord
    new_grid = deepcopy(grid)
    possible_directions = []
    if x > 1 and new_grid[x - 1][y] == "■":
        possible_directions.append("up")
    if y < len(new_grid[0]) - 2 and new_grid[x][y + 1] == "■":
        possible_directions.append("right")
    if x < len(new_grid) - 2 and new_grid[x + 1][y] == "■":
        possible_directions.append("down")
    if y > 1 and new_grid[x][y - 1] == "■":
        possible_directions.append("left")
    if not possible_directions:
        return new_grid
    direction = possible_directions[0]
    if direction == "up":
        new_grid[x - 1][y] = " "
    elif direction == "right":
        new_grid[x][y + 1] = " "
    elif direction == "down":
        new_grid[x + 1][y] = " "
    elif direction == "left":
        new_grid[x][y - 1] = " "
    return new_grid


def bin_tree_maze(rows=15, cols=15):
    grid = create_grid(rows, cols)
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "
            directions = []
            if x > 1:
                directions.append((-1, 0))
            if y > 1:
                directions.append((0, -1))
            if directions:
                dx, dy = directions[0]  # берем строго первое направление
                grid[x + dx][y + dy] = " "
    grid[0][0] = "X"
    grid[rows - 1][cols - 1] = "X"
    return grid


def get_exits(grid: List[List[Cell]]) -> List[Tuple[int, int]]:
    return [(x, y) for x, row in enumerate(grid) for y, c in enumerate(row) if c == "X"]


def make_step(grid: List[List[Cell]], k: int) -> List[List[Cell]]:
    new_coords = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == k:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                        new_coords.append((nx, ny))
    for nx, ny in new_coords:
        if grid[nx][ny] == 0:
            grid[nx][ny] = k + 1
    return grid


def shortest_path(grid: List[List[Cell]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    path: List[Tuple[int, int]] = [exit_coord]
    cur_coord: Tuple[int, int] = exit_coord
    cur_cell = grid[cur_coord[0]][cur_coord[1]]
    if not isinstance(cur_cell, int):
        return None
    cur_value: int = cur_cell

    while cur_value != 1:
        neighbors: List[Tuple[int, int]] = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cur_coord[0] + dx, cur_coord[1] + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbor_cell = grid[nx][ny]
                if isinstance(neighbor_cell, int) and neighbor_cell == cur_value - 1:
                    neighbors.append((nx, ny))

        if not neighbors:
            grid[cur_coord[0]][cur_coord[1]] = " "
            path.pop()
            if not path:
                return None
            cur_coord = path[-1]
            cur_cell = grid[cur_coord[0]][cur_coord[1]]
            if not isinstance(cur_cell, int):
                return None
            cur_value = cur_cell
        else:
            cur_coord = neighbors[0]
            cur_cell = grid[cur_coord[0]][cur_coord[1]]
            if not isinstance(cur_cell, int):
                return None
            cur_value = cur_cell
            path.append(cur_coord)

    return path


def encircled_exit(grid: List[List[Cell]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != "■":
            return False
    return True


def solve_maze(grid: List[List[Cell]]) -> Tuple[List[List[Cell]], Optional[List[Tuple[int, int]]]]:
    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None
    for an_exit in exits:
        if encircled_exit(grid, an_exit):
            return grid, None

    start_coord, end_coord = exits
    q_grid = deepcopy(grid)

    for r in range(len(q_grid)):
        for c in range(len(q_grid[0])):
            if q_grid[r][c] == " " or q_grid[r][c] == "X":
                q_grid[r][c] = 0

    q_grid[start_coord[0]][start_coord[1]] = 1
    k = 1

    while q_grid[end_coord[0]][end_coord[1]] == 0:
        prev = deepcopy(q_grid)
        make_step(q_grid, k)
        if q_grid == prev:
            return grid, None
        k += 1

    path = shortest_path(q_grid, end_coord)
    if path is None:
        return grid, None
    return grid, path


def add_path_to_grid(grid: List[List[Cell]], path: Optional[List[Tuple[int, int]]]) -> List[List[Cell]]:
    if path:
        for x, y in path:
            grid[x][y] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
