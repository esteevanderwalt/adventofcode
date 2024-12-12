import re
from itertools import combinations

puzzle_input = [i.strip() for i in open(r'input.txt', 'r').readlines()]
length = len(puzzle_input[0])
width = len(puzzle_input)
string = ''.join(puzzle_input)
possible_characters = set(string)


def in_bounds(coords: complex):
    return int(coords.real) in range(length) and int(coords.imag) in range(width)


def get_element(coords: complex) -> str:
    return puzzle_input[int(coords.imag)][int(coords.real)]


def get_blocks(coordinate: complex):
    matched = []
    to_match = get_element(coordinate)

    def blocks_recursive(coordinate: complex, to_match: str):
        nonlocal matched
        if coordinate in matched:
            return
        matched.append(coordinate)
        for i in range(4):
            new_element = coordinate-(1j)**i
            if in_bounds(new_element) and get_element(new_element) == to_match:
                blocks_recursive(new_element, to_match)
        return
    blocks_recursive(coordinate, to_match)
    return matched


regions = []
print(possible_characters)
for character in possible_characters:
    coordinates = [complex(*divmod(i, width)[::-1]) for i in (i.start() for i in re.finditer(character, string))]
    for coord in coordinates:
        if coord not in [coord for region in regions for coord in region]:
            regions.append(get_blocks(coord))


def part1():
    cost = 0
    for region in regions:
        surroundings = [(i, (1j) ** _) for i in region for _ in range(4) if i + (1j) ** _ not in region]
        perimeter = len(surroundings)
        area = len(region)
        cost += perimeter*area
    return cost


def part2():
    cost = 0
    for region in regions:
        surroundings = [(i, (1j)**_ ) for i in region for _ in range(4) if i+(1j)**_ not in region]
        count = 0
        plausible_differences = [1, 1j, -1, -1j]
        for element1, element2 in combinations(surroundings, 2):
            if element1[0]-element2[0] in plausible_differences and element1[1] == element2[1]:
                count += 1
        sides = len(surroundings)-count
        area = len(region)
        cost += sides*area
    return cost


print(part1())
print(part2())
