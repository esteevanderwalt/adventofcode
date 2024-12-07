# You receive a 2D input where
# - obstacles are indicated by '#'
# - guards are indicated by a caret '^' where the direction of the caret indicates the direction the guard is facing

# You need to find the distinct positions where the guard has visited.
# Rules:
# - The guard starts at its current position
# - The guard moves in the direction it is facing until it hits an obstacle or reaches the end of the grid
# - The guard then turns 90 degrees to its right and moves in that direction
# - The guard repeats this process until it reaches the end of the grid and leaves the grid

# However, the new challenge is to introduce a new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

import copy

def read_grid_from_file(file_path):
    with open(file_path, 'r') as file:
        # Read each line, strip the newline character, and create a list of lists
        grid = [list(line.strip()) for line in file if line.strip()]
    return grid


# Function to move the guard and detect cycles, if there is a cycle, return True
def move_guard_with_cycle_check(grid, start_row, start_col, direction) -> bool:
    directions = {
        '^': (-1, 0),  # Up
        '>': (0, 1),   # Right
        'v': (1, 0),   # Down
        '<': (0, -1)   # Left
    }
    turns = ['^', '>', 'v', '<']  # Order of turns: Up -> Right -> Down -> Left
    visited = set()  # Positions visited by the guard
    seen_states = set()  # Track (row, col, direction) to detect cycles

    row, col = start_row, start_col
    prev_state = None

    while True:
        # print(f"Guard at ({row}, {col}) facing {direction}")
        # Mark the current position as visited
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            visited.add((row, col))

        # Save current state to detect cycles
        state = (row, col, direction)
        if state in seen_states:
            # print(f"Cycle detected at state: {state}. Stopping.")
            return True
        seen_states.add(state)

        # If the guard hasn't moved and keeps turning, break
        if state == prev_state:
            return True
        prev_state = state

        # Move in the current direction
        dr, dc = directions[direction]
        next_row, next_col = row + dr, col + dc

        # print(f"Next position: ({next_row}, {next_col})")
        # Check if the move is valid
        if (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]) and grid[next_row][next_col] != '#'):
            row, col = next_row, next_col  # Continue moving
        else:
            if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
                # print(f"Guard at ({row}, {col}) hit the end of the grid.")
                break

            # Turn 90 degrees to the right
            direction = turns[(turns.index(direction) + 1) % 4]

            # Check the next position after turning
            dr, dc = directions[direction]
            next_row, next_col = row + dr, col + dc

            if (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]) and grid[next_row][next_col] != '#'):
                row, col = next_row, next_col  # Move in the new direction
            else:
                # print(f"Guard at ({row}, {col}) hit an obstacle or reached the end of the grid after turning.")
                # Guard is stuck and exits
                break

    return False


def get_all_visited_positions(grid):
    # First find the guards position
    count_cycles = 0
    guard_row, guard_col, guard_cell = None, None, None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in '^>v<':  # If it's a guard
                # print(f"Processing guard at ({r}, {c}) facing {cell}")
                guard_row, guard_col, guard_cell = r, c, cell
                cycle = move_guard_with_cycle_check(grid, guard_row, guard_col, guard_cell)     
                if cycle:
                    count_cycles += 1
                break
        if guard_row is not None:
            break

    # cn = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '.':
                # cn += 1
                tmp_grid = copy.deepcopy(grid)
                tmp_grid[r][c] = '#'
                cycle = move_guard_with_cycle_check(tmp_grid, guard_row, guard_col, guard_cell)     
                if cycle:
                    count_cycles += 1
            # if cn == 5:
            #     print(tmp_grid)
            #     return count_cycles

    # print(f"Total distinct positions visited: {len(visited_positions)}")
    return count_cycles


# Get the grid from the input file
grid = read_grid_from_file("test_input.txt")
print("Grid size:", len(grid), "x", len(grid[0]))

cycles = get_all_visited_positions(grid)
# print("Ordered Visited Positions:", sorted(visited))
print("Visited Positions:", cycles)
