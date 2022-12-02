from typing import List


TEST_INPUT = """A Y
B X
C Z"""

shape_scores = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

outcome_scores = {
    "X": {"A": 3, "B": 0, "C": 6},
    "Y": {"A": 6, "B": 3, "C": 0},
    "Z": {"A": 0, "B": 6, "C": 3},
}

choices = {
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}


def total_score(input: List) -> int:
    """Calculate the total score for the given input."""
    total = 0
    for line in input:
        opponent_choice, my_choice = line.split()
        total += shape_scores[my_choice]
        total += outcome_scores[my_choice][opponent_choice]
    return total


def score_given_choice(input: List) -> int:
    """Calculate the score for the given input, given a choice."""
    total = 0
    for line in input:
        opponent_choice, outcome = line.split()
        my_choice = choices[outcome][opponent_choice]
        total += shape_scores[my_choice]
        total += outcome_scores[my_choice][opponent_choice]
    return total


test_input = TEST_INPUT.splitlines()
assert total_score(test_input) == 15
assert score_given_choice(test_input) == 12

with open("input.txt") as f:
    input_list = f.read().splitlines()
    print(total_score(input_list))
    print(score_given_choice(input_list))
