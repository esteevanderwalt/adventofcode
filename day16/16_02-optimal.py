import heapq
from typing import List, Tuple, Set

def parse_maze(file_path: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    """Parse the maze input from a file."""
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

def heuristic(pos: Tuple[int, int], end: Tuple[int, int]) -> int:
    """Calculate the Manhattan distance heuristic."""
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def is_valid(grid: List[List[str]], x: int, y: int) -> bool:
    """Check if the position is within bounds and not a wall."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

def find_best_paths(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Find all tiles part of at least one best path."""
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left

    rows, cols = len(grid), len(grid[0])

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, 0, start, 1, []))  # (total_cost, g_cost, position, direction, path)

    # Track best paths and minimum cost
    best_paths = []
    min_cost = float('inf')

    # Visited dictionary: stores the minimum cost for each position
    visited = {}

    while pq:
        total_cost, g_cost, (x, y), dir_idx, path = heapq.heappop(pq)

        # Prune paths that exceed the best-known cost
        if g_cost > min_cost:
            continue

        # If we reach the end, update best paths
        if (x, y) == end:
            if g_cost < min_cost:
                min_cost = g_cost
                best_paths = [path + [(x, y)]]
            elif g_cost == min_cost:
                best_paths.append(path + [(x, y)])
            continue

        # Allow revisiting the position with the same g_cost
        if (x, y) in visited:
            if visited[(x, y)] <= g_cost:
                continue  # If we have visited this cell with a better or equal cost, skip it

        visited[(x, y)] = g_cost

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
            heapq.heappush(pq, (new_total_cost, new_g_cost, (nx, ny), new_dir_idx, path + [(x, y)]))

    # Aggregate all tiles from best paths
    best_path_tiles = set()
    for path in best_paths:
        best_path_tiles.update(path)

    return best_path_tiles

def mark_best_path_tiles(grid: List[List[str]], best_path_tiles: Set[Tuple[int, int]]):
    """Mark the tiles part of the best paths with 'O'."""
    for x, y in best_path_tiles:
        if grid[x][y] not in ('S', 'E'):
            grid[x][y] = 'O'

def print_grid(grid: List[List[str]]):
    """Print the maze grid."""
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your maze input file
    grid, start, end = parse_maze(input_file)
    best_path_tiles = find_best_paths(grid, start, end)
    mark_best_path_tiles(grid, best_path_tiles)
    print_grid(grid)
    print("Number of tiles part of best paths:", len(best_path_tiles))
