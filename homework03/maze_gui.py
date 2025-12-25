import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

from maze import add_path_to_grid, bin_tree_maze, solve_maze

CELL_SIZE = 10


def draw_cell(x, y, color, size: int = CELL_SIZE):
    x *= size
    y *= size
    canvas.create_rectangle(x, y, x + size, y + size, fill=color)


def draw_maze(grid: List[List[str]], size: int = CELL_SIZE):
    canvas.delete("all")
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            color = "white" if cell == " " else "black" if cell == "■" else "purple"
            draw_cell(y, x, color, size)


def show_solution():
    maze_copy, path = solve_maze(GRID)
    maze_copy = add_path_to_grid(GRID, path)
    if path:
        draw_maze(maze_copy, CELL_SIZE)
    else:
        messagebox.showinfo("Message", "No solution")


if __name__ == "__main__":
    N, M = 51, 77
    GRID = bin_tree_maze(N, M)
    _, PATH = solve_maze(GRID)
    while not PATH:
        GRID = bin_tree_maze(N, M)
        _, PATH = solve_maze(GRID)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{M * CELL_SIZE + 100}x{N * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
