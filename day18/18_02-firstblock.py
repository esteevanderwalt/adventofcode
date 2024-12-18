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

class UnionFind:
    """Union-Find data structure with path compression and union by rank."""
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def coord_to_index(x, y, grid_size):
    """Convert 2D coordinates to a 1D index for Union-Find."""
    return y * grid_size + x


def find_first_blocking_byte(grid_size, byte_positions):
    """Optimized function to find the first blocking byte."""
    uf = UnionFind(grid_size * grid_size)
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start_index = coord_to_index(0, 0, grid_size)
    goal_index = coord_to_index(grid_size - 1, grid_size - 1, grid_size)

    for i, (x, y) in enumerate(byte_positions):
        grid[y][x] = "#"  # Mark the cell as corrupted

        # Union adjacent non-corrupted cells
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[ny][nx] == ".":
                uf.union(coord_to_index(x, y, grid_size), coord_to_index(nx, ny, grid_size))

        # Check if start and goal are still connected
        if not uf.connected(start_index, goal_index):
            return x, y

    return None  # No blocking byte found


def main():
    file_path = "input.txt"  # Replace with your file path
    grid_size = 71  # Example grid size

    byte_positions = read_positions(file_path)

    blocking_byte = find_first_blocking_byte(grid_size, byte_positions)
    if blocking_byte:
        print(f"The first byte that blocks the path is at: {blocking_byte[0]},{blocking_byte[1]}")
    else:
        print("No byte completely blocks the path.")


if __name__ == "__main__":
    main()
