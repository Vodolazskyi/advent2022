from typing import Dict, Tuple
from copy import deepcopy


TEST_INPUT = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def parse_input(input: str) -> Tuple[Dict[int, list], list]:
    """Parse the input into stacks and a list of moves."""
    stacks = {}
    moves = []
    stacks_raw, moves_raw = input.split("\n\n")
    moves = moves_raw.splitlines()
    for row in stacks_raw.splitlines()[::-1]:
        if row.strip().startswith("["):
            for i in range(0, len(row), 4):
                if value := row[i : i + 4].strip().strip("[]"):
                    stacks.setdefault(i // 4, []).append(value)
    return stacks, moves


def make_moves(stacks: Dict[int, list], moves: list) -> Dict[int, list]:
    """Make the moves on the stacks."""
    new_stacks = deepcopy(stacks)
    for move in moves:
        move_from_stack, to_stack = move.split("to")
        from_stack = int(move_from_stack.split("from")[1].strip()) - 1
        amount = int(move_from_stack.split("from")[0].strip().split("move")[1].strip())
        to_stack = int(to_stack.strip()) - 1
        for _ in range(amount):
            new_stacks[to_stack].append(new_stacks[from_stack].pop())
    return new_stacks


def make_moves_at_once(stacks: Dict[int, list], moves: list) -> Dict[int, list]:
    """Make the moves on the stacks."""
    new_stacks = deepcopy(stacks)
    for move in moves:
        move_from_stack, to_stack = move.split("to")
        from_stack = int(move_from_stack.split("from")[1].strip()) - 1
        amount = int(move_from_stack.split("from")[0].strip().split("move")[1].strip())
        to_stack = int(to_stack.strip()) - 1
        new_stacks[to_stack].extend(new_stacks[from_stack][-amount:])
        new_stacks[from_stack] = new_stacks[from_stack][:-amount]
    return new_stacks


def top_stack(stacks: Dict[int, list]) -> str:
    """Find and concat the top stack."""
    return "".join(stacks[i][-1] for i in range(len(stacks)) if stacks[i])


test_stacks, test_moves = parse_input(TEST_INPUT)
test_stacks_simple = make_moves(test_stacks, test_moves)
test_stacks_at_once = make_moves_at_once(test_stacks, test_moves)
assert top_stack(test_stacks_simple) == "CMZ"
assert top_stack(test_stacks_at_once) == "MCD"

with open("input.txt") as f:
    stacks, moves = parse_input(f.read())
    stacks_simple = make_moves(stacks, moves)
    print(top_stack(stacks_simple))
    stacks_at_once = make_moves_at_once(stacks, moves)
    print(top_stack(stacks_at_once))
