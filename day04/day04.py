from typing import List

TEST_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def count_full_overlap_sections(sections: List) -> int:
    """Count the number of overlapping sections in a list of sections."""
    result = 0
    for pair in sections:
        first, second = pair.split(",")
        first_start, first_end = first.split("-")
        second_start, second_end = second.split("-")
        if (
            int(first_start) >= int(second_start) and int(first_end) <= int(second_end)
        ) or (
            int(first_start) <= int(second_start) and int(first_end) >= int(second_end)
        ):
            result += 1
    return result


def count_partial_overlap_sections(sections: List) -> int:
    """Count the number of partially overlapping sections in a list of sections."""
    result = 0
    for pair in sections:
        first, second = pair.split(",")
        first_start, first_end = (int(x) for x in first.split("-"))
        second_start, second_end = (int(x) for x in second.split("-"))
        first_range = set(range(first_start, first_end + 1))
        second_range = set(range(second_start, second_end + 1))
        if first_range.intersection(second_range):
            result += 1
    return result


test_sections = TEST_INPUT.splitlines()

assert count_full_overlap_sections(test_sections) == 2
assert count_partial_overlap_sections(test_sections) == 4

with open("input.txt") as f:
    sections = f.read().splitlines()
    print(count_full_overlap_sections(sections))
    print(count_partial_overlap_sections(sections))
