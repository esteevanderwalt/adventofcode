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

from collections import Counter


def read_stones(file_path):
    """Reads the initial stones from the file and returns them as a Counter."""
    with open(file_path, 'r') as f:
        stones = [int(x) for x in f.readline().split()]
    return Counter(stones)


def simulate_turn(stone_counts):
    """Simulates one turn and returns the updated stone counts."""
    new_stone_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == 0:
            # Replace with a stone engraved with 1
            new_stone_counts[1] += count
        elif len(str(stone)) % 2 == 0:
            # Split into two stones if the number of digits is even
            stone_str = str(stone)
            mid = len(stone_str) // 2
            left = int(stone_str[:mid])
            right = int(stone_str[mid:])
            new_stone_counts[left] += count
            new_stone_counts[right] += count
        else:
            # Replace with a stone engraved with stone * 2024
            new_stone_counts[stone * 2024] += count

    return new_stone_counts


def simulate_stones(file_path, turns):
    """Simulates the stones for the given number of turns."""
    stone_counts = read_stones(file_path)

    for _ in range(turns):
        stone_counts = simulate_turn(stone_counts)

    return sum(stone_counts.values())


def main():
    stone_file = "input.txt"
    turns = 75

    result = simulate_stones(stone_file, turns)
    print(f"Number of stones after {turns} turns: {result}")


if __name__ == "__main__":
    main()


# Avoid Creating Large Lists:
# Instead of creating a new list for every turn, use generators or append results incrementally to manage memory more efficiently.
# Optimize Stone Splitting:
# Precompute digit splits or optimize operations on numbers to minimize expensive string conversions.
# Track Stone Counts:
# Use a dictionary or counter-like structure to track stones and their counts instead of storing them in a list. This avoids repeated handling of identical values.
# Batch Processing:
# Process stones in batches to avoid repeatedly iterating over the entire collection.

# Edited Stone Simulation

# Improvements Made
# Use of Counter:
# Instead of handling a list of stones, we track the count of each stone value using Python's Counter. This reduces memory usage and speeds up operations by avoiding duplicates.
# Efficient Simulation:
# The simulate_turn function iterates through the stone types and their counts, performing transformations while directly updating the new stone counts.
# Batch Processing:
# By processing all stones of the same type in batches, the algorithm minimizes overhead from repeatedly processing identical stones.
# Scalable Calculation:
# The total number of stones is computed by summing the counts in the Counter, avoiding the need to rebuild large lists.