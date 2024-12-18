import heapq
from collections import deque

def read_positions(file_path):
    """Read the byte positions from a file."""
    with open(file_path, 'r') as file:
        positions = [tuple(map(int, line.strip().split(','))) for line in file]
    return positions

def simulate_corruption(grid_size, byte_positions, num_bytes):
    """Simulate the corruption of the grid based on byte positions."""
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    
    for x, y in byte_positions[:num_bytes]:
        grid[y][x] = "#"

    return grid

def print_grid(grid):
    """Print the grid."""
    for row in grid:
        print("".join(row))

def is_valid(x, y, grid, visited):
    """Check if a position is valid for movement."""
    n = len(grid)
    return 0 <= x < n and 0 <= y < n and grid[y][x] != "#" and (x, y) not in visited

def find_shortest_path(grid):
    """Find the shortest path using BFS."""
    n = len(grid)
    start = (0, 0)
    goal = (n - 1, n - 1)

    if grid[0][0] == "#" or grid[n - 1][n - 1] == "#":
        return float('inf')  # No valid path

    queue = deque([(0, 0, 0)])  # (x, y, steps)
    visited = set()
    visited.add((0, 0))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == goal:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, grid, visited):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return float('inf')  # No path found

def main():
    file_path = "input.txt"  # Replace with your file path
    grid_size = 71  # Example grid size
    num_bytes = 1024  # Simulating the first kilobyte

    byte_positions = read_positions(file_path)
    grid = simulate_corruption(grid_size, byte_positions, num_bytes)

    print("Grid after corruption:")
    print_grid(grid)

    shortest_path = find_shortest_path(grid)
    if shortest_path == float('inf'):
        print("No path to the exit exists.")
    else:
        print(f"The shortest path to the exit is {shortest_path} steps.")

if __name__ == "__main__":
    main()
