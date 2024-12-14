# Define the space dimensions and time to simulate
SPACE_WIDTH = 101
SPACE_HEIGHT = 103
SIMULATION_TIME = 100

# Function to parse the input file
def parse_input_file(filename):
    robots = []
    with open(filename, "r") as file:
        for line in file:
            # Parse positions and velocities from each line
            parts = line.strip().split(" ")
            position = list(map(int, parts[0][2:].split(",")))
            velocity = list(map(int, parts[1][2:].split(",")))
            robots.append({"p": position, "v": velocity})
    return robots

# Function to update position with wrapping
def update_position(position, velocity, width, height):
    x = (position[0] + velocity[0]) % width
    y = (position[1] + velocity[1]) % height
    return [x, y]

# Function to simulate robots and count quadrants
def simulate_and_count(filename):
    robots = parse_input_file(filename)

    # Simulate the robot movements
    for _ in range(SIMULATION_TIME):
        for robot in robots:
            robot["p"] = update_position(robot["p"], robot["v"], SPACE_WIDTH, SPACE_HEIGHT)

    # Count robots in quadrants
    quadrant_counts = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    for robot in robots:
        x, y = robot["p"]
        if x == SPACE_WIDTH // 2 or y == SPACE_HEIGHT // 2:
            # Robots on the middle lines don't count in any quadrant
            continue
        if x > SPACE_WIDTH // 2 and y < SPACE_HEIGHT // 2:
            quadrant_counts["Q1"] += 1
        elif x < SPACE_WIDTH // 2 and y < SPACE_HEIGHT // 2:
            quadrant_counts["Q2"] += 1
        elif x < SPACE_WIDTH // 2 and y > SPACE_HEIGHT // 2:
            quadrant_counts["Q3"] += 1
        elif x > SPACE_WIDTH // 2 and y > SPACE_HEIGHT // 2:
            quadrant_counts["Q4"] += 1

    # Print results
    print("Robots in each quadrant after 100 seconds:")
    total_safety = 1
    for quadrant, count in quadrant_counts.items():
        print(f"{quadrant}: {count}")
        total_safety *= count
    print(f"Total safety: {total_safety}")


# Main Execution
if __name__ == "__main__":
    input_filename = "input.txt"  # Replace with your input file name
    simulate_and_count(input_filename)
