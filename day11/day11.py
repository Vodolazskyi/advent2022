from typing import List, Dict


class Monkey:
    def __init__(
        self,
        items: List[int],
        operation: str,
        test: int,
        test_true: int,
        test_false: int,
    ):
        self.items = items
        self.operation = operation
        self.test = test
        self.test_true = test_true
        self.test_false = test_false
        self.inspected_items = 0

    def __repr__(self) -> str:
        return f"Monkey(items={self.items})"

    def add_item(self, item: int):
        self.items.append(item)

    def take_turn(
        self,
        monkey_dict: Dict[int, "Monkey"],
        modulus: int,
        relief: int = 3,
    ):
        for _ in range(len(self.items)):
            old = self.items.pop(0)
            new = eval(self.operation)
            new_item = new // relief
            new_item = new_item % modulus
            if new_item % self.test == 0:
                monkey_dict[self.test_true].add_item(new_item)
            else:
                monkey_dict[self.test_false].add_item(new_item)
            self.inspected_items += 1


def parse_monkey(monkey_input: str) -> Monkey:
    items = []
    operation = ""
    test = 0
    test_true = 0
    test_false = 0
    for line in monkey_input.splitlines():
        line = line.strip()
        if line.startswith("Starting"):
            items = [int(x) for x in line.split(":")[-1].split(",")]
        elif line.startswith("Operation"):
            operation = line.split("=")[-1].strip()
        elif line.startswith("Test"):
            test = int(line.split("by")[-1].strip())
        elif line.startswith("If true"):
            test_true = int(line.split("to monkey")[-1].strip())
        elif line.startswith("If false"):
            test_false = int(line.split("to monkey")[-1].strip())
    return Monkey(items, operation, test, test_true, test_false)


def level_monkey_business(input: str, n_rounds: int, relief: int = 3) -> int:
    """
    Make 20 rounds of monkey business and
    return the product of 2 highest inspected items.
    """
    monkey_dict = {}
    modulus = 1
    for idx, monkey_input in enumerate(input.split("\n\n")):
        monkey = parse_monkey(monkey_input)
        monkey_dict[idx] = monkey
        modulus *= monkey.test
    for _ in range(n_rounds):
        for monkey in monkey_dict.values():
            monkey.take_turn(monkey_dict, modulus, relief)
    inspected_items = sorted(
        [monkey.inspected_items for monkey in monkey_dict.values()]
    )
    return inspected_items[-1] * inspected_items[-2]


with open("test_input.txt") as f:
    test_input = f.read()
    assert level_monkey_business(test_input, n_rounds=20, relief=3) == 10605
    assert level_monkey_business(test_input, n_rounds=10000, relief=1) == 2713310158

with open("input.txt") as f:
    input_text = f.read()
    print(level_monkey_business(input_text, n_rounds=20, relief=3))
    print(level_monkey_business(input_text, n_rounds=10000, relief=1))
