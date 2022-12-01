TEST_INPUT = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

test_calories = [[int(x) for x in line.split()] for line in TEST_INPUT.split("\n\n")]


def get_maximum_calories(calories_list):
    """Sum calories in each list and return the maximum value"""
    return max(sum(x) for x in calories_list)


def get_top_three_calories(calories_list):
    """Return the sum of top three total calories"""
    return sum(sorted(sum(x) for x in calories_list)[-3:])


assert get_maximum_calories(test_calories) == 24000
assert get_top_three_calories(test_calories) == 45000

with open("input.txt") as f:
    calories = [[int(x) for x in line.split()] for line in f.read().split("\n\n")]

print(get_maximum_calories(calories))
print(get_top_three_calories(calories))
