import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    return group([c for c in pathlib.Path(path).read_text() if c in "123456789."], 9)


def display(grid: tp.List[tp.List[str]]) -> None:
    w = 2
    line = "+".join(["-" * (w * 3)] * 3)
    for r in range(9):
        print("".join(grid[r][c].center(w) + ("|" if c in (2, 5) else "") for c in range(9)))
        if r in (2, 5):
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i * n : (i + 1) * n] for i in range(n)]


def get_row(g, p):
    return g[p[0]]


def get_col(g, p):
    return [r[p[1]] for r in g]


def get_block(g, p):
    r, c = p
    br, bc = (r // 3) * 3, (c // 3) * 3
    return [g[br + i][bc + j] for i in range(3) for j in range(3)]


def find_empty_positions(g):
    return next(((r, c) for r in range(9) for c in range(9) if g[r][c] == "."), None)


def find_possible_values(g, p):
    return set("123456789") - set(get_row(g, p)) - set(get_col(g, p)) - set(get_block(g, p))


def solve(g):
    p = find_empty_positions(g)
    if p is None:
        return g
    r, c = p
    for v in find_possible_values(g, p):
        g[r][c] = v
        if solve(g):
            return g
        g[r][c] = "."
    return None


def check_solution(s):
    e = set("123456789")
    return all(
        set(get_row(s, (i, 0))) == e and set(get_col(s, (0, i))) == e for i in range(9)
    ) and all(set(get_block(s, (r, c))) == e for r in (0, 3, 6) for c in (0, 3, 6))


def generate_sudoku(N: int):
    g = solve([["."] * 9 for _ in range(9)])
    N = max(0, min(N, 81))
    pos = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(pos)
    for r, c in pos[N:]:
        g[r][c] = "."
    return g


if __name__ == "__main__":
    for f in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        g = read_sudoku(f)
        display(g)
        s = solve(g)
        if s:
            display(s)
        else:
            print(f"Puzzle {f} can't be solved")
