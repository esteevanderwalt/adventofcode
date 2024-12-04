# You need to read data from a file into a two dimensional array
# Set a counter to 0
# everytime you find an X, you should validate whether XMAS is found
# If it is found, increment the counter by 1

def read_file_to_2d_array(file_path):
    """Reads the file and converts it into a 2D array."""
    with open(file_path, 'r') as file:
        array = [list(line.strip()) for line in file.readlines()]
    return array


def validate_xmas(array, x, y):
    """Checks if 'XMAS' exists starting from position (x, y) in any direction."""
    directions = [
        (0, 1),    # Horizontal right
        (0, -1),   # Horizontal left
        (1, 0),    # Vertical down
        (-1, 0),   # Vertical up
        (1, 1),    # Diagonal down-right
        (-1, 1),   # Diagonal up-right
        (1, -1),   # Diagonal down-left
        (-1, -1),  # Diagonal up-left
    ]
    word = "XMAS"
    rows, cols = len(array), len(array[0])
    count = 0  # Count occurrences for this starting point

    for dx, dy in directions:
        found = True
        for i in range(len(word)):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or ny < 0 or nx >= rows or ny >= cols or array[nx][ny] != word[i]:
                found = False
                break
        if found:
            count += 1
    return count


def count_xmas_occurrences(file_path):
    """Counts the occurrences of 'XMAS' in the 2D array."""
    array = read_file_to_2d_array(file_path)
    total_counter = 0

    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 'X':  # Start checking only if the character is 'X'
                total_counter += validate_xmas(array, i, j)
    return total_counter


file_path = 'input.txt'
count = count_xmas_occurrences(file_path)
print(f"Total occurrences of 'XMAS': {count}")
