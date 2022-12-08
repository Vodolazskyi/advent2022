from typing import List


TEST_INPUT = """30373
25512
65332
33549
35390"""


def parse_input(input: str) -> List[List[int]]:
    return [[int(tree) for tree in line] for line in input.splitlines()]


def count_visible_trees(grid: List[List[int]]) -> int:
    visible_trees = (len(grid) + len(grid[0]) - 2) * 2
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            tree = grid[row][col]
            left = grid[row][:col]
            visible_left = all(left_tree < tree for left_tree in left)
            top = grid[:row]
            visible_top = all(top_row[col] < tree for top_row in top)
            right = grid[row][col + 1 :]
            visible_right = all(right_tree < tree for right_tree in right)
            bottom = grid[row + 1 :]
            visible_bottom = all(bottom_row[col] < tree for bottom_row in bottom)
            if any((visible_left, visible_top, visible_right, visible_bottom)):
                visible_trees += 1
    return visible_trees


def highest_scenic_score(grid: List[List[int]]) -> int:
    highest_score = 0
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            left_score = 0
            top_score = 0
            right_score = 0
            bottom_score = 0
            tree = grid[row][col]
            left = grid[row][:col]
            for left_tree in left[::-1]:
                left_score += 1
                if left_tree >= tree:
                    break
            top = grid[:row]
            for top_row in top[::-1]:
                top_score += 1
                if top_row[col] >= tree:
                    break
            right = grid[row][col + 1 :]
            for right_tree in right:
                right_score += 1
                if right_tree >= tree:
                    break
            bottom = grid[row + 1 :]
            for bottom_row in bottom:
                bottom_score += 1
                if bottom_row[col] >= tree:
                    break
            score = left_score * top_score * right_score * bottom_score
            if score > highest_score:
                highest_score = score
    return highest_score


test_grid = parse_input(TEST_INPUT)
assert count_visible_trees(test_grid) == 21
assert highest_scenic_score(test_grid) == 8

with open("input.txt") as f:
    grid = parse_input(f.read())
    print(count_visible_trees(grid))
    print(highest_scenic_score(grid))
