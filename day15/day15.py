from typing import Tuple
from dataclasses import dataclass
import re
import tqdm


TEST_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


Point = Tuple[int, int]
point_rgx = r"x=(\-?[0-9]+), y=(\-?[0-9]+)"


@dataclass
class Sensor:
    position: Point
    beacon: Point

    def __post_init__(self) -> None:
        self.manhattan = abs(self.position[0] - self.beacon[0]) + abs(
            self.position[1] - self.beacon[1]
        )

    @staticmethod
    def from_string(s: str) -> "Sensor":
        (x1, y1), (x2, y2) = re.findall(point_rgx, s)
        return Sensor((int(x1), int(y1)), (int(x2), int(y2)))


@dataclass
class Range:
    lo: int
    hi: int

    def __post_init__(self) -> None:
        self.length = self.hi - self.lo + 1


def find_free_points(
    sensors: list[Sensor],
    row: int,
) -> list[Range]:
    ranges = []
    for sensor in sensors:
        distance = sensor.manhattan
        diff_y = abs(row - sensor.position[1])
        diff_x = distance - diff_y
        if diff_x < 0:
            continue
        lo_x = sensor.position[0] - diff_x
        hi_x = sensor.position[0] + diff_x
        ranges.append(Range(lo_x, hi_x))
    ranges = sorted(ranges, key=lambda r: r.lo)

    # Merge overlapping ranges
    new_ranges = []
    while ranges:
        r = ranges.pop(0)
        if not new_ranges:
            new_ranges.append(r)
        elif r.lo <= new_ranges[-1].hi + 1:
            new_ranges[-1] = Range(new_ranges[-1].lo, max(r.hi, new_ranges[-1].hi))
        else:
            new_ranges.append(r)
    return new_ranges


def find_free_points_in_range(
    sensors: list[Sensor], row: int, min_x: int, max_x: int
) -> list[Range]:
    ranges = find_free_points(sensors, row)
    ranges = [Range(max(min_x, r.lo), min(max_x, r.hi)) for r in ranges]
    return ranges


def count_free_points(sensors: list[Sensor], row: int) -> int:
    beacons = {sensor.beacon[0] for sensor in sensors if sensor.beacon[1] == row}
    ranges = find_free_points(sensors, row)
    return sum(r.length for r in ranges) - len(beacons)


def find_distress_beacon_freq(sensors: list[Sensor], min_lim: int, max_lim: int) -> int:
    x, y = min_lim, min_lim
    for y in tqdm.trange(min_lim, max_lim + 1):
        ranges = find_free_points_in_range(sensors, y, min_lim, max_lim)
        if len(ranges) <= 1:
            continue
        x = ranges[0].hi + 1
        break
    return x * 4_000_000 + y


test_sensors = [Sensor.from_string(s) for s in TEST_INPUT.splitlines()]
assert count_free_points(test_sensors, 10) == 26
assert find_distress_beacon_freq(test_sensors, 0, 20) == 56000011


with open("input.txt") as f:
    input_str = f.read()
    sensors = [Sensor.from_string(s) for s in input_str.splitlines()]
    print(count_free_points(sensors, 2_000_000))
    print(find_distress_beacon_freq(sensors, 0, 4_000_000))
