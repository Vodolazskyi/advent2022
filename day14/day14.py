from typing import Set, Generator


TEST_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


Point = tuple[int, int]
Cave = Set[Point]


def draw_line(p1: Point, p2: Point) -> Generator:
    if p1[0] == p2[0]:
        range_gen = (
            range(p1[1], p2[1] + 1) if p1[1] < p2[1] else range(p1[1], p2[1] - 1, -1)
        )
        for y in range_gen:
            yield p1[0], y
    elif p1[1] == p2[1]:
        range_gen = (
            range(p1[0], p2[0] + 1) if p1[0] < p2[0] else range(p1[0], p2[0] - 1, -1)
        )
        for x in range_gen:
            yield x, p1[1]
    else:
        raise ValueError("Not a horizontal or vertical line")


def make_cave(input: str) -> Cave:
    cave = set()
    for line in input.splitlines():
        points = [
            (int(x), int(y)) for x, y in [p.split(",") for p in line.split(" -> ")]
        ]
        for p1, p2 in zip(points, points[1:]):
            for x, y in draw_line(p1, p2):
                cave.add((x, y))
    return cave


def pouring_sand(cave: Cave, block_source: bool = False) -> int:
    cave = cave.copy()
    source = (500, 0)
    rest = 0
    if block_source:
        lowest_rock = max(cave, key=lambda p: p[1])[1] + 2
    else:
        lowest_rock = max(cave, key=lambda p: p[1])[1]
    pos = source
    while pos[1] < lowest_rock:
        if block_source and pos[1] + 1 == lowest_rock:
            cave.add((pos[0], pos[1]))
            rest += 1
            pos = source
        elif (pos[0], pos[1] + 1) not in cave:
            pos = (pos[0], pos[1] + 1)
        elif (pos[0] - 1, pos[1] + 1) not in cave:
            pos = (pos[0] - 1, pos[1] + 1)
        elif (pos[0] + 1, pos[1] + 1) not in cave:
            pos = (pos[0] + 1, pos[1] + 1)
        else:
            if block_source and pos == source:
                rest += 1
                return rest
            cave.add(pos)
            rest += 1
            pos = source
    return rest


test_cave = make_cave(TEST_INPUT)
assert pouring_sand(test_cave) == 24
assert pouring_sand(test_cave, block_source=True) == 93


with open("input.txt") as f:
    input_cave = make_cave(f.read())
    print(pouring_sand(input_cave))
    print(pouring_sand(input_cave, block_source=True))
