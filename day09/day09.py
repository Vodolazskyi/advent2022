from dataclasses import dataclass


TEST_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Point(self.x + other, self.y + other)
        else:
            raise TypeError("Invalid type for addition.")

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Point(self.x - other, self.y - other)
        else:
            raise TypeError("Invalid type for subtraction.")

    def normalize(self):
        if self.x == 0 and self.y == 0:
            return self
        elif self.x == 0:
            return Point(0, self.y // abs(self.y))
        elif self.y == 0:
            return Point(self.x // abs(self.x), 0)
        else:
            return Point(self.x // abs(self.x), self.y // abs(self.y))


def count_visited(input: str, length: int) -> int:
    """Count the number of visited locations by the tail of the rope."""
    motions = input.splitlines()
    visited = {(0, 0)}
    rope = [Point(0, 0) for _ in range(length)]
    for motion in motions:
        direction, steps = motion[0], int(motion[1:])
        for _ in range(steps):
            if direction == "R":
                rope[0] = rope[0] + Point(1, 0)
            elif direction == "L":
                rope[0] = rope[0] + Point(-1, 0)
            elif direction == "U":
                rope[0] = rope[0] + Point(0, 1)
            elif direction == "D":
                rope[0] = rope[0] + Point(0, -1)
            for i in range(1, length):
                distance = rope[i - 1] - rope[i]
                if abs(distance.x) > 1 or abs(distance.y) > 1:
                    rope[i] = rope[i] + distance.normalize()
            visited.add((rope[-1].x, rope[-1].y))  # type: ignore
    return len(visited)


assert count_visited(TEST_INPUT, 2) == 13
assert count_visited(TEST_INPUT, 10) == 1


with open("input.txt") as f:
    moitions = f.read()
    print(count_visited(moitions, 2))
    print(count_visited(moitions, 10))
