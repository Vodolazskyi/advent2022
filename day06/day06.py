START_OF_PACKET = 4
START_OF_MESSAGE = 14

TEST_INPUTS = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": {START_OF_PACKET: 7, START_OF_MESSAGE: 19},
    "bvwbjplbgvbhsrlpgdmjqwftvncz": {START_OF_PACKET: 5, START_OF_MESSAGE: 23},
    "nppdvjthqldpwncqszvftbrmjlhg": {START_OF_PACKET: 6, START_OF_MESSAGE: 23},
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": {START_OF_PACKET: 10, START_OF_MESSAGE: 29},
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": {START_OF_PACKET: 11, START_OF_MESSAGE: 26},
}


def detect_start(datastream: str, distinct_chars: int) -> int:
    """Detect the first marker."""
    for i in range(len(datastream)):
        if len(set(datastream[i : i + distinct_chars])) == distinct_chars:
            return i + distinct_chars
    return -1


for datastream, expected in TEST_INPUTS.items():
    for distinct_chars, expected_result in expected.items():
        assert detect_start(datastream, distinct_chars) == expected_result


with open("input.txt") as f:
    datastream = f.read().strip()
    print(detect_start(datastream, START_OF_PACKET))
    print(detect_start(datastream, START_OF_MESSAGE))
