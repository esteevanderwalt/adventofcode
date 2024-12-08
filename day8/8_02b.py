from collections.abc import Sequence
import itertools as it


def read_input_from_file(file_path):
    """Reads the input grid from a file and returns it as a list of strings."""
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file if line.strip()]
    return grid


def get_antennas(
        grid: Sequence[Sequence[str]],
) -> dict[str, list[tuple[int, int]]]:
    """
    Get the frequency and locations of each antenna in a grid.
    """
    antennas: dict[str, list[tuple[int, int]]] = {}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == ".":
                continue
            antennas.setdefault(char, []).append((r, c))

    return antennas


def aoc2024_day08_part1(grid: Sequence[Sequence[str]],
                        antennas: dict[str, list[tuple[int, int]]]) -> int:
    height, width = len(grid), len(grid[0])

    antinodes: set[tuple[int, int]] = set()
    for locations in antennas.values():
        for (r1, c1), (r2, c2) in it.combinations(locations, r=2):
            # These diffs are for jumping from antenna 1 to antenna 2
            row_diff, column_diff = r2 - r1, c2 - c1

            # Jumping backwards from antenna 1 gives an antinode
            r1 -= row_diff
            c1 -= column_diff
            if 0 <= r1 < height and 0 <= c1 < width:
                antinodes.add((r1, c1))

            # Jumping forwards from antenna 2 gives an antinode
            r2 += row_diff
            c2 += column_diff
            if 0 <= r2 < height and 0 <= c2 < width:
                antinodes.add((r2, c2))

    return len(antinodes)


def aoc2024_day08_part2(grid: Sequence[Sequence[str]],
                        antennas: dict[str, list[tuple[int, int]]]) -> int:
    height, width = len(grid), len(grid[0])

    antinodes: set[tuple[int, int]] = set()
    for locations in antennas.values():
        for (r1, c1), (r2, c2) in it.combinations(locations, r=2):
            # These diffs are for jumping from antenna 1 to antenna 2
            row_diff, column_diff = r2 - r1, c2 - c1

            # Jumping backwards from antenna 1 gives antinodes
            while 0 <= r1 < height and 0 <= c1 < width:
                antinodes.add((r1, c1))
                r1 -= row_diff
                c1 -= column_diff

            # Jumping forwards from antenna 2 gives antinodes
            while 0 <= r2 < height and 0 <= c2 < width:
                antinodes.add((r2, c2))
                r2 += row_diff
                c2 += column_diff

    return len(antinodes)


# Input example
input_grid = read_input_from_file('input.txt')
antennas = get_antennas(input_grid)

parts = (aoc2024_day08_part1(input_grid, antennas),
         aoc2024_day08_part2(input_grid, antennas))

print(*parts, sep='\n')