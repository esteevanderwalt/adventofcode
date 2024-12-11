# Stone are arranged in a perfectly straight line, and each stone has a number engraved on it
# At each turn, these stones change simultaniously based on the following rules:
# - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# - If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. 
# The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved 
# on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number 
# multiplied by 2024 is engraved on the new stone.

# Your task is to find the number of stones after x amount of turns

# Steps:
# 1. Read the initial stones from the file
# 2. Simulate the turns
# 3. Print the number of stones after x turns

import sys


def read_stones(file_path):
    """Reads the initial stones from the file and returns them as a list of integers."""
    with open(file_path, 'r') as f:
        return [int(x) for x in f.readline().split()]


def simulate_turn(stones):
    """Simulates one turn and returns the new list of stones."""
    new_stones = []

    for stone in stones:
        if stone == 0:
            # Replace with a stone engraved with 1
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            # Split into two stones if the number of digits is even
            stone_str = str(stone)
            mid = len(stone_str) // 2
            left = int(stone_str[:mid])
            right = int(stone_str[mid:])
            new_stones.append(left)
            new_stones.append(right)
        else:
            # Replace with a stone engraved with stone * 2024
            new_stones.append(stone * 2024)

    return new_stones


def simulate_stones(file_path, turns):
    """Simulates the stones for the given number of turns."""
    stones = read_stones(file_path)

    for _ in range(turns):
        stones = simulate_turn(stones)

    return len(stones)


def main():
    stone_file = "input.txt"
    turns = 25

    result = simulate_stones(stone_file, turns)
    print(f"Number of stones after {turns} turns: {result}")


if __name__ == "__main__":
    main()
