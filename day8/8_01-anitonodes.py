# You are tasked with analyzing a map of antennas to determine how many unique locations within the bounds of the map contain an antinode.

# Definitions:
# Antennas:
# Each antenna is tuned to a specific frequency, represented by a single character (a-z, A-Z, or 0-9).
# Characters with different cases (e.g., A and a) or different values (e.g., 1 and 2) represent different frequencies.

# Antinode:
# An antinode is a point on the map that is perfectly aligned with two antennas of the same frequency, where one antenna is exactly twice as far away from the antinode as the other.
# For a pair of antennas with the same frequency, there are two antinodes: one on each side of the pair.

# Rules:
# Antennas of different frequencies do not interact to create antinodes.
# Antinodes can occur at locations containing antennas if the conditions above are satisfied.
# Antinodes outside the bounds of the map are ignored.
# The task is to calculate the total number of unique positions on the map that contain antinodes.

# Input Format:
# The input is a 2D grid of characters, with:
# . representing empty space.
# A single character (a-z, A-Z, or 0-9) representing an antenna.

# Output:
# The program should output the number of unique locations that contain antinodes within the bounds of the map.

def read_input_from_file(file_path):
    """Reads the input grid from a file and returns it as a list of strings."""
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file if line.strip()]
    return grid


def parse_map(grid):
    """Parse the map and locate the antennas by frequency."""
    antennas = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '.':
                if cell not in antennas:
                    antennas[cell] = []
                antennas[cell].append((r, c))
    return antennas


def calculate_collinear_points(x1, y1, x2, y2):
    """
    Calculate two new points such that all four points form a straight line, 
    equally distanced from each other.

    Parameters:
    x1, y1: Coordinates of the first point
    x2, y2: Coordinates of the second point

    Returns:
    Two new points (x0, y0) and (x3, y3)
    """
    # Calculate the distance between the original points
    dx = x2 - x1
    dy = y2 - y1

    # Calculate the length of the segment
    segment_length = (dx**2 + dy**2)**0.5

    # Normalize the vector (dx, dy) to find unit direction
    unit_dx = dx / segment_length
    unit_dy = dy / segment_length

    # Calculate the two new points
    # Point before (x1, y1)
    x0 = x1 - segment_length * unit_dx
    y0 = y1 - segment_length * unit_dy

    # Point after (x2, y2)
    x3 = x2 + segment_length * unit_dx
    y3 = y2 + segment_length * unit_dy

    return x0, y0, x3, y3


def calculate_antinodes(antenna_positions, map_size):
    """Calculate all valid antinodes for a specific frequency."""
    rows, cols = map_size
    antinodes = set()

    for i in range(len(antenna_positions)):
        for j in range(i + 1, len(antenna_positions)):
            ax, ay = antenna_positions[i]
            bx, by = antenna_positions[j]

            # print(f"Antenna A: {ax}, {ay}")
            # print(f"Antenna B: {bx}, {by}")
            cx, cy, dx, dy = calculate_collinear_points(ax, ay, bx, by)
            if 0 <= cx < rows and 0 <= cy < cols:
                antinodes.add((int(cx), int(cy)))
            if 0 <= dx < rows and 0 <= dy < cols:
                antinodes.add((int(dx), int(dy)))

    return antinodes


def count_unique_antinodes(grid):
    """Main function to calculate the total number of unique antinodes."""
    antennas = parse_map(grid)
    rows, cols = len(grid), len(grid[0])
    unique_antinodes = set()

    for frequency, positions in antennas.items():
        antinodes = calculate_antinodes(positions, (rows, cols))
        unique_antinodes.update(antinodes)

    return len(unique_antinodes)


# Input example
input_grid = read_input_from_file('input.txt')

# Process the input
result = count_unique_antinodes(input_grid)
print(f"Total unique antinodes: {result}")