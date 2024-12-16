# Next challenge to solve: you receive a maze in a file. 
# Read this input from the file. Your task is to find the most cost effective route to get from the start (S) to the end (E). 
# You cannot walk through walls (#). Each moves counts 1 point and each turn counts 1000 points. 
# You can only rotate clockwise or counterclockwise 90 degrees at a time

import heapq

def parse_maze(file_path):
    """Parse the maze from the input file."""
    with open(file_path, 'r') as f:
        grid = [list(line.strip()) for line in f]
    start, end = None, None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return grid, start, end

def heuristic(pos, end):
    """Calculate the Manhattan distance heuristic."""
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def is_valid(grid, x, y):
    """Check if the position is within bounds and not a wall."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

def find_path(grid, start, end):
    """Find the most cost-effective path using A*."""
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    direction_names = ['U', 'R', 'D', 'L']
    rows, cols = len(grid), len(grid[0])

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, 0, start, 1))  # (total_cost, g_cost, position, direction)

    # Visited set to track (position, direction)
    visited = set()

    while pq:
        total_cost, g_cost, (x, y), dir_idx = heapq.heappop(pq)

        # If we reach the end, return the cost
        if (x, y) == end:
            return total_cost

        # Skip if already visited
        if ((x, y), dir_idx) in visited:
            continue
        visited.add(((x, y), dir_idx))

        # Explore neighbors
        for new_dir_idx, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy

            # Check if the new position is valid
            if not is_valid(grid, nx, ny):
                continue

            # Calculate costs
            move_cost = 1
            turn_cost = 1000 if new_dir_idx != dir_idx else 0
            new_g_cost = g_cost + move_cost + turn_cost
            new_total_cost = new_g_cost + heuristic((nx, ny), end)

            # Add to priority queue
            heapq.heappush(pq, (new_total_cost, new_g_cost, (nx, ny), new_dir_idx))

    return -1  # No path found


if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your maze input file
    grid, start, end = parse_maze(input_file)
    result = find_path(grid, start, end)
    print("Minimum cost to reach the end:", result)
