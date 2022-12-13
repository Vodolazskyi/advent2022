from itertools import zip_longest


TEST_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def find_right_pairs(input: str) -> int:
    pairs = input.split("\n\n")
    sum_indicies = 0
    for i, pair in enumerate(pairs):
        left, right = pair.strip().split("\n")
        left = eval(left)
        right = eval(right)
        if is_right_order(left, right):
            sum_indicies += i + 1
    return sum_indicies


def sort_packets(input: str) -> int:
    """Sort packets by their order."""
    packets = [eval(packet) for packet in input.split()]
    divider1 = [[2]]
    divider2 = [[6]]
    packets += [divider1, divider2]
    packets_sorted = []
    while packets:
        packet = packets.pop(0)
        if not packets_sorted:
            packets_sorted.append(packet)
        else:
            for i, packet_sorted in enumerate(packets_sorted):
                if is_right_order(packet, packet_sorted):
                    packets_sorted.insert(i, packet)
                    break
            else:
                packets_sorted.append(packet)
    return (packets_sorted.index(divider1) + 1) * (packets_sorted.index(divider2) + 1)


def is_right_order(left: list, right: list) -> bool:
    for l_i, r_i in zip_longest(left, right):
        if isinstance(l_i, list) and isinstance(r_i, list):
            try:
                return is_right_order(l_i, r_i)
            except ValueError:
                continue
        elif isinstance(l_i, int) and isinstance(r_i, int):
            if l_i < r_i:
                return True
            elif l_i > r_i:
                return False
            else:
                continue
        elif l_i is None:
            return True
        elif r_i is None:
            return False
        else:
            l_i = [l_i] if isinstance(l_i, int) else l_i
            r_i = [r_i] if isinstance(r_i, int) else r_i
            try:
                return is_right_order(l_i, r_i)
            except ValueError:
                continue
    raise ValueError("No valid order found")


assert find_right_pairs(TEST_INPUT) == 13
assert sort_packets(TEST_INPUT) == 140

with open("input.txt") as f:
    data = f.read()
    print(find_right_pairs(data))
    print(sort_packets(data))
