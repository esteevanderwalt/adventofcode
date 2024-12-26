# Do the following steps:
# 1. Read input from a file. The input contains a grid of a map of boxes where X is a wall and O is a box. 
# The remainder of the file is a series of moves that the robot (@) makes. Example input:

# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<

# 2. Find the robot to know where to Start  
# 3. Execute the moves (move the robot) and also follow the following rules:
#     - If the robot hits a wall, it should stop and not move any further.
#     - If the robot hits a box, it should push the box in the direction it is moving. 
#     - If the robot hits a box and the box hits a wall, the robot should stop and not move any further.
#     - If the robot hits a box and the box hits another box, the robot should move all connected boxes by one only if its possible

# 4. Calculate the final score by:
#     - each box = 100 * (number of steps from the top) + (number of steps from the left)
#     - sum all the boxes scores

from typing import List, Tuple


def parse_input(file_path: str) -> Tuple[List[List[str]], str]:
    """Parses the input file into a grid and a series of moves."""
    with open(file_path, 'r') as f:
        lines = f.read().strip().split("\n")
    grid = [list(line) for line in lines[:-1]]
    moves = lines[-1]
    return grid, moves


def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
    """Finds the robot's starting position (@) in the grid."""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                return i, j
    raise ValueError("Robot not found in the grid.")


def move_robot(grid: List[List[str]], moves: str) -> int:
    """Executes the moves and calculates the final score."""
    directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    robot_pos = find_robot(grid)

    def is_wall(x: int, y: int) -> bool:
        return grid[x][y] == '#'

    def can_move_box(x: int, y: int, dx: int, dy: int) -> bool:
        """Checks if a box at (x, y) can be moved in direction (dx, dy)."""
        while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            x += dx
            y += dy
            if is_wall(x, y):
                return False
            if grid[x][y] == '.':
                return True
        return False

    def push_box(x: int, y: int, dx: int, dy: int) -> bool:
        """Attempts to push a box at (x, y) in direction (dx, dy)."""
        to_push = []
        while grid[x][y] == 'O':
            to_push.append((x, y))
            x += dx
            y += dy

        if is_wall(x, y) or grid[x][y] == 'O':
            return False

        for bx, by in reversed(to_push):
            grid[bx][by] = '.'
        for bx, by in to_push:
            bx += dx
            by += dy
            grid[bx][by] = 'O'
        return True

    # Capture grid states for visualization
    grid_states = []

    for idx, move in enumerate(moves):
        dx, dy = directions[move]
        new_x, new_y = robot_pos[0] + dx, robot_pos[1] + dy

        if is_wall(new_x, new_y):
            grid_states.append((idx + 1, move, [row.copy() for row in grid]))
            continue

        if grid[new_x][new_y] == 'O':
            if push_box(new_x, new_y, dx, dy):
                grid[robot_pos[0]][robot_pos[1]] = '.'
                grid[new_x][new_y] = '@'
                robot_pos = (new_x, new_y)
        elif grid[new_x][new_y] == '.':
            grid[robot_pos[0]][robot_pos[1]] = '.'
            grid[new_x][new_y] = '@'
            robot_pos = (new_x, new_y)

        # Save grid state for every move
        grid_states.append((idx + 1, move, [row.copy() for row in grid]))

    def print_grids_side_by_side(grids: List[Tuple[int, str, List[List[str]]]]):
        """Prints multiple grid states side by side."""
        rows = len(grids[0][2])
        for row in range(rows):
            print("    ".join("".join(grid[2][row]) for grid in grids))
        print("    ".join(f"Move {grid[0]} ({grid[1]})" for grid in grids))
        print()

    # Print grids in batches of 5
    batch_size = 5
    for i in range(0, len(grid_states), batch_size):
        batch = grid_states[i:i + batch_size]
        print_grids_side_by_side(batch)

    def calculate_score() -> int:
        """Calculates the final score based on box positions."""
        score = 0
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 'O':
                    score += 100 * i + j
        return score

    return calculate_score()


if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file path
    grid, moves = parse_input(input_file)
    final_score = move_robot(grid, moves)
    print("Final Score:", final_score)
