from string import ascii_lowercase as alphabet
from typing import List


TEST_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


priorities = {}
for i, letter in enumerate(alphabet):
    priorities[letter] = i + 1
    priorities[letter.upper()] = i + 27


def sum_priorities(rucksacks: List) -> int:
    result = 0
    for rucksack in rucksacks:
        first = set(rucksack[: len(rucksack) // 2])
        second = set(rucksack[len(rucksack) // 2 :])
        result += sum(priorities[letter] for letter in first & second)
    return result


def sum_priorities_in_groups(rucksacks: List) -> int:
    result = 0
    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i : i + 3]
        first = set(group[0])
        second = set(group[1])
        third = set(group[2])
        result += sum(priorities[letter] for letter in first & second & third)
    return result


test_rucksacks = TEST_INPUT.splitlines()

assert sum_priorities(test_rucksacks) == 157
assert sum_priorities_in_groups(test_rucksacks) == 70

with open("input.txt") as f:
    rucksacks = f.read().splitlines()
    print(sum_priorities(rucksacks))
    print(sum_priorities_in_groups(rucksacks))
