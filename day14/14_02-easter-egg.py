# Define the space dimensions
SPACE_WIDTH = 101
SPACE_HEIGHT = 103

# Define the hardcoded Christmas tree pattern
CHRISTMAS_TREE_PATTERN = [
    "   #   ",
    "  ###  ",
    " ##### ",
    "#######",
    "   #   "
]

def parse_input_file(filename):
    robots = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            position = list(map(int, parts[0][2:].split(",")))
            velocity = list(map(int, parts[1][2:].split(",")))
            robots.append({"p": position, "v": velocity})
    return robots

def update_position_with_wrap(position, velocity, width, height):
    x = (position[0] + velocity[0]) % width
    y = (position[1] + velocity[1]) % height
    return [x, y]

def calculate_bounding_box(robots):
    xs = [robot["p"][0] for robot in robots]
    ys = [robot["p"][1] for robot in robots]
    return (min(xs), max(xs), min(ys), max(ys))

def check_pattern_match(robots, bounding_box):
    """Check if robots match the Christmas tree pattern."""
    min_x, max_x, min_y, max_y = bounding_box
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Verify the bounding box dimensions match the pattern
    if width != len(CHRISTMAS_TREE_PATTERN[0]) or height != len(CHRISTMAS_TREE_PATTERN):
        return False

    # Create a set of robot positions
    robot_positions = {(robot["p"][0] - min_x, robot["p"][1] - min_y) for robot in robots}

    # Check against the pattern
    for y, row in enumerate(CHRISTMAS_TREE_PATTERN):
        for x, char in enumerate(row):
            if char == "#" and (x, y) not in robot_positions:
                return False
            if char == " " and (x, y) in robot_positions:
                return False

    return True

def display_robots(robots, bounding_box):
    """Visualize the robot positions within the bounding box."""
    min_x, max_x, min_y, max_y = bounding_box
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for robot in robots:
        x, y = robot["p"]
        if min_x <= x <= max_x and min_y <= y <= max_y:
            grid[y - min_y][x - min_x] = "#"
    for row in grid:
        print("".join(row))
    print()

def find_christmas_tree(filename):
    """Simulate robot movements and detect patterns."""
    robots = parse_input_file(filename)
    seconds = 0

    while True:
        # Update robot positions with wrapping
        for robot in robots:
            robot["p"] = update_position_with_wrap(robot["p"], robot["v"], SPACE_WIDTH, SPACE_HEIGHT)

        seconds += 1

        # Calculate the bounding box of current positions
        bounding_box = calculate_bounding_box(robots)
        width = bounding_box[1] - bounding_box[0] + 1
        height = bounding_box[3] - bounding_box[2] + 1

        # Skip if bounding box is too large to match the pattern
        # if width > len(CHRISTMAS_TREE_PATTERN[0]) or height > len(CHRISTMAS_TREE_PATTERN):
        #     continue

        # Display compact robot positions and ask for confirmation
        print(f"Potential compact pattern detected after {seconds} seconds:")
        display_robots(robots, bounding_box)

        # Ask user for confirmation
        user_input = input("Does this look like a Christmas tree? (y/n): ").lower()
        if user_input == "y":
            print("Easter egg (Christmas tree) confirmed!")
            return seconds
        elif user_input == "n":
            print("Continuing simulation...")
        else:
            print("Invalid input. Continuing simulation...")

# Main Execution
if __name__ == "__main__":
    input_filename = "input.txt"  # Replace with your input file name
    seconds = find_christmas_tree(input_filename)
    print(f"Easter egg (Christmas tree) confirmed after {seconds} seconds!")
