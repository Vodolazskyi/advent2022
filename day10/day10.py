from typing import Tuple


TEST_IMAGE = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


def signal_strength_and_image(input: str) -> Tuple[int, str]:
    commands = input.splitlines()
    strength = 0
    X = 1
    cycles = 0
    add_cycles = {
        "noop": 1,
        "addx": 2,
    }
    crt_pos = 0
    image = []
    crt_row = ""
    for command in commands:
        instruction = command.split()[0]
        for _ in range(add_cycles[instruction]):
            cycles += 1
            if cycles == 20 or cycles % 40 == 20:
                strength += X * cycles
            crt_row += "#" if crt_pos in [X - 1, X, X + 1] else "."
            crt_pos += 1
            if cycles % 40 == 0:
                image.append(crt_row)
                crt_row = ""
                crt_pos = 0
        if instruction == "addx":
            X += int(command.split()[1])
            # print(f"{cycles=}: {X=}")
    return strength, "\n".join(image)


with open("test_input.txt") as f:
    test_input = f.read()
    strength, image = signal_strength_and_image(test_input)
    assert strength == 13140
    for test_row, row in zip(TEST_IMAGE.splitlines(), image.splitlines()):
        assert test_row == row


with open("input.txt") as f:
    input_text = f.read()
    strength, image = signal_strength_and_image(input_text)
    print(strength)
    print(image)
