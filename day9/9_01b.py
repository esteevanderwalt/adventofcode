from itertools import count
from copy import deepcopy


def solve_day(my_file):
    data = parse_data(my_file)
    print('Part 1: ', part1(deepcopy(data)))
    print('Part 2: ', part2(data))


def parse_data(my_file) -> list:
    with open(my_file) as f:
        return [int(num) for num in f.read().strip()]
    

def part1(data: list) -> int:
    total = 0
    pos = count()
    last_file = len(data)//2
    last_len = data.pop()
    for idx, block in enumerate(data):
        for _ in range(block):
            current = next(pos)
            if idx % 2:
                if not last_len:
                    try:
                        data.pop()
                        last_len = data.pop()
                        last_file -= 1
                    except IndexError:
                        break
                total += current*last_file
                last_len -= 1
            else:
                total += current * (idx//2)
    for _ in range(last_len):
        total += next(pos)*last_file
    return total


def part2(data: list) -> int:
    total = 0
    pos = count()
    used = set()
    for idx, block in enumerate(data):
        if idx not in used and idx % 2:
            while block:
                for r_ind in range(len(data)-1, idx,-2):
                    if r_ind not in used and data[r_ind] <= block:
                        last_len = data[r_ind]
                        last_file = r_ind//2
                        used.add(r_ind)
                        break
                else:
                    last_len = block
                    last_file = 0
                for _ in range(last_len):
                    current = next(pos)
                    total += current*last_file
                    block -= 1
        else:
            last_file = 0 if idx in used else idx//2
            for _ in range(block):
                current = next(pos)
                total += current*last_file
    return total


solve_day('input.txt')
