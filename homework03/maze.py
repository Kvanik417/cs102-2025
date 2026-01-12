from copy import deepcopy
from random import choice, randint
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
    direction = choice(possible_directions)
    if direction == "up":
        new_grid[x - 1][y] = " "
    elif direction == "right":
        new_grid[x][y + 1] = " "
    elif direction == "down":
        new_grid[x + 1][y] = " "
    elif direction == "left":
        new_grid[x][y - 1] = " "
    return new_grid

def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Cell]]:
    grid = create_grid(rows, cols)
    empty_cells: List[Tuple[int, int]] = []
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = " "
            empty_cells.append((x, y))
    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_go_up = x > 1
        can_go_right = y < cols - 2
        if direction == "up" and can_go_up:
            grid[x - 1][y] = " "
        elif direction == "right" and can_go_right:
            grid[x][y + 1] = " "
        elif can_go_up:
            grid[x - 1][y] = " "
        elif can_go_right:
            grid[x][y + 1] = " "
    def pick_exit() -> Tuple[int, int]:
        candidates = (
            [(0, y) for y in range(cols)]
            + [(rows - 1, y) for y in range(cols)]
            + [(x, 0) for x in range(rows)]
            + [(x, cols - 1) for x in range(rows)]
        )
        return choice(candidates)
    if random_exit:
        x_in, y_in = pick_exit()
        x_out, y_out = pick_exit()
        while (x_in, y_in) == (x_out, y_out):
            x_out, y_out = pick_exit()
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"
    return grid

def get_exits(grid: List[List[Cell]]) -> List[Tuple[int, int]]:
    return [(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row) if cell == "X"]

def make_step(grid: List[List[Cell]], k: int) -> List[List[Cell]]:
    indices = [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == k]
    for x, y in indices:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                grid[nx][ny] = k + 1
    return grid

def shortest_path(grid: List[List[Cell]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    path = [exit_coord]
    cur_coord = exit_coord
    cur_value = grid[cur_coord[0]][cur_coord[1]]
    if not isinstance(cur_value, int):
        return None
    while cur_value != 1:
        neighbors = [
            (cur_coord[0] + dx, cur_coord[1] + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= cur_coord[0] + dx < len(grid)
            and 0 <= cur_coord[1] + dy < len(grid[0])
            and grid[cur_coord[0] + dx][cur_coord[1] + dy] == cur_value - 1
        ]
        if not neighbors:
            grid[cur_coord[0]][cur_coord[1]] = " "
            path.pop()
            if not path:
                return None
            cur_coord = path[-1]
            cur_value = grid[cur_coord[0]][cur_coord[1]]
        else:
            cur_coord = neighbors[0]
            cur_value = grid[cur_coord[0]][cur_coord[1]]
            path.append(cur_coord)
    return path

def encircled_exit(grid: List[List[Cell]], coord: Tuple[int, int]]) -> bool:
    x, y = coord
    free_neighbors = sum(
        1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]) and grid[x + dx][y + dy] == " "
    )
    return free_neighbors == 0

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
            if q_grid[r][c] == " ":
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
