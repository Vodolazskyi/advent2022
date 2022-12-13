from collections import deque
from string import ascii_lowercase
from typing import Tuple


TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

chars = f"S{ascii_lowercase}E"
LEVELS = {char: i for i, char in enumerate(chars)}


def make_grid(input: str) -> dict[Tuple[int, int], str]:
    """Make a grid from the input."""
    lines = input.splitlines()
    grid = {}
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            grid[(r, c)] = char
    return grid


def find_path(grid: dict[Tuple[int, int], str], starting_chars: list[str]) -> int:
    """Find the shortest path"""
    starting_positions = [pos for pos in grid if grid[pos] in starting_chars]
    paths = []
    for pos in starting_positions:
        queue: deque[Tuple[Tuple[int, int], int]] = deque([(pos, 0)])
        visited = {pos}
        while queue:
            pos, steps = queue.popleft()
            if grid[pos] == "E":
                paths.append(steps)
                break
            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in visited:
                    continue
                if new_pos in grid and LEVELS[grid[new_pos]] - LEVELS[grid[pos]] <= 1:
                    queue.append((new_pos, steps + 1))
                    visited.add(new_pos)

    return min(paths)


test_grid = make_grid(TEST_INPUT)
assert find_path(test_grid, ["S"]) == 31
assert find_path(test_grid, ["S", "a"]) == 29


with open("input.txt") as f:
    grid = make_grid(f.read())
    print(find_path(grid, ["S"]))
    print(find_path(grid, ["S", "a"]))
