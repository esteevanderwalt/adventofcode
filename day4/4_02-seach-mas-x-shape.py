# You need to read data from a file into a two dimensional array
# Set a counter to 0
# everytime you find an X, you should validate whether XMAS is found
# If it is found, increment the counter by 1

# Further instructions:
# Adjust the algorithm to count occurrences of "MAS" that overlap in an "X" shape
# The idea is to start with 'A' and check if 'MAS' is found diagonally only.

def read_file_to_2d_array(file_path):
    """Reads the file and converts it into a 2D array."""
    with open(file_path, 'r') as file:
        array = [list(line.strip()) for line in file.readlines()]
    return array


def validate_x_shape(array, x, y):
    """Validates if there is an 'MAS' X-shape with 'A' at (x, y)."""
    rows, cols = len(array), len(array[0])

    # Ensure the central character is 'A'
    if array[x][y] != 'A':
        return 0

    # Check if the X-shape pattern is within bounds
    if x - 1 < 0 or x + 1 >= rows or y - 1 < 0 or y + 1 >= cols:
        return 0

    d = [array[x - 1][y - 1], array[x + 1][y + 1], array[x + 1][y - 1], array[x - 1][y + 1]]
    # Validate the X-shape pattern
    if (
        (d[0] == 'M' and d[1] == 'S' and d[2] == 'M' and d[3] == 'S')
        or
        (d[0] == 'S' and d[1] == 'M' and d[2] == 'S' and d[3] == 'M')
        or
        (d[0] == 'M' and d[1] == 'S' and d[2] == 'S' and d[3] == 'M')
        or
        (d[0] == 'S' and d[1] == 'M' and d[2] == 'M' and d[3] == 'S')
    ):
        return 1

    return 0


def count_x_shapes(file_path):
    """Counts the number of 'MAS' X-shapes in the 2D array."""
    array = read_file_to_2d_array(file_path)
    total_counter = 0

    # Iterate over each position in the array
    for i in range(len(array)):
        for j in range(len(array[0])):
            # Validate for the X-shape with 'A' at (i, j)
            total_counter += validate_x_shape(array, i, j)

    return total_counter


file_path = 'input.txt'
count = count_x_shapes(file_path)
print(f"Total occurrences of 'XMAS': {count}")
