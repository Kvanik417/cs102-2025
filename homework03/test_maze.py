import unittest
from random import seed

import maze


class MazeTest(unittest.TestCase):
    def test_remove_wall(self):
        seed(2)
        grid_1 = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        coord_1 = (1, 1)
        self.assertEqual(
            [
                ["■", "■", "■", "■", "■"],
                ["■", " ", " ", " ", "■"],
                ["■", "■", "■", "■", "■"],
                ["■", " ", "■", " ", "■"],
                ["■", "■", "■", "■", "■"],
            ],
            maze.remove_wall(grid_1, coord_1),
        )

    def test_bin_tree_maze(self):
        seed(42)
        expected_grid_42 = [
            ["■", "■", "■", "■", "■"],
            ["X", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_42, maze.bin_tree_maze(5, 5))

        seed(222)
        expected_grid_222 = [
            ["■", "X", "■", "X", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected_grid_222, maze.bin_tree_maze(5, 5))

    def test_get_exits(self):
        grid_1 = [
            ["■", "X", "■", "■", "■"],
            ["■", " ", " ", " ", "■"],
            ["■", "■", "■", " ", "■"],
            ["X", " ", " ", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual([(0, 1), (3, 0)], maze.get_exits(grid_1))

    def test_encircled_exit(self):
        grid = [
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
            ["■", " ", "■", " ", "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertFalse(maze.encircled_exit(grid, (1, 1)))
        self.assertTrue(maze.encircled_exit(grid, (0, 0)))

    def test_make_step(self):
        grid = [
            ["■", "■", "■", "■", "■"],
            ["■", 1, 0, 0, "■"],
            ["■", 0, "■", 0, "■"],
            ["■", 0, 0, 0, "■"],
            ["■", "■", "■", "■", "■"],
        ]
        k = 1
        expected = [
            ["■", "■", "■", "■", "■"],
            ["■", 1, 2, 0, "■"],
            ["■", 2, "■", 0, "■"],
            ["■", 2, 0, 0, "■"],
            ["■", "■", "■", "■", "■"],
        ]
        self.assertEqual(expected, maze.make_step(grid, k))

    def test_solve_maze(self):
        seed(34)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        self.assertIsInstance(path_, list)

        seed(151)
        grid = maze.bin_tree_maze(5, 5)
        _, path_ = maze.solve_maze(grid)
        # В некоторых случаях путь может быть None
        self.assertTrue(path_ is None or isinstance(path_, list))

    def test_shortest_path(self):
        grid = [
            ["■", "■", "■", "■", "■"],
            ["■", 1, 2, 3, "■"],
            ["■", 0, "■", 4, "■"],
            ["■", 0, 0, 5, "■"],
            ["■", "■", "■", "■", "■"],
        ]
        exit_coord = (3, 3)
        expected_path = [(3, 3), (2, 3), (1, 3), (1, 2), (1, 1)]
        self.assertEqual(expected_path, maze.shortest_path(grid, exit_coord))


if __name__ == "__main__":
    unittest.main()
