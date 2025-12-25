import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    _, col = pos
    return [grid[r][col] for r in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    return [
        grid[r][c]
        for r in range(start_row, start_row + 3)
        for c in range(start_col, start_col + 3)
    ]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ".":
                return (r, c)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    used = set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))
    return set("123456789") - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    r, c = empty
    for value in find_possible_values(grid, (r, c)):
        grid[r][c] = value
        solution = solve(grid)
        if solution:
            return solution
        grid[r][c] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(9):
        row = get_row(solution, (i, 0))
        col = get_col(solution, (0, i))
        if '.' in row or '.' in col:
            return False
        for j in range(1, 10):
            if row.count(str(j)) > 1 or col.count(str(j)) > 1:
                return False
    for r in [0, 3, 6]:
        for c in [0, 3, 6]:
            block = get_block(solution, (r, c))
            if '.' in block:
                return False
            for j in range(1, 10):
                if block.count(str(j)) > 1:
                    return False
    return True



def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    from random import shuffle
    grid = solve([["."]*9 for _ in range(9)])
    positions = [(r, c) for r in range(9) for c in range(9)]
    shuffle(positions)
    for r, c in positions[N:]:
        grid[r][c] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)