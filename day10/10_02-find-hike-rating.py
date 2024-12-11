# You are presented with a map. The map is a topography where each number indicates the height.
# You task is to map a hiking route. 
# You determine that a good hiking trail is 
# as long as possible and has an even, gradual, uphill slope. For all practical purposes, 
# this means that a hiking trail is any path that starts at height 0, ends at height 9, 
# and always increases by a height of exactly 1 at each step. Hiking trails never include 
# diagonal steps - only up, down, left, or right (from the perspective of the map).
# The positions marked . are impassable tiles

# A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, 
# you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail.

# Steps:
# 1. Read the map from the file
# 2. Find all the trailheads (height 0)
# 3. For each trailhead, find all the 9-height positions reachable from that trailhead
# 4. Calculate the score for each trailhead
# 5. Print the sum of all trailhead scores

# Adjustment:
# The paper describes a second way to measure a trailhead called its rating. 
# A trailhead's rating is the number of distinct hiking trails which begin at that trailhead

from collections import deque


def read_map(file_path):
    """Reads the map from the file and returns it as a list of lists."""
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f]


def find_trailheads(map_data):
    """Find all positions with height 0."""
    trailheads = []
    for r, row in enumerate(map_data):
        for c, cell in enumerate(row):
            if cell == '0':
                trailheads.append((r, c))
    return trailheads


def find_score(map_data, start):
    """Calculate the score for a single trailhead."""
    rows, cols = len(map_data), len(map_data[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    visited = set()
    queue = deque([(start[0], start[1], 0)])  # (row, col, current height)
    reachable_nines = set()

    while queue:
        r, c, height = queue.popleft()

        # Skip if already visited
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Check if we reached height 9
        if map_data[r][c] == '9':
            reachable_nines.add((r, c))

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Ensure within bounds and valid movement
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if map_data[nr][nc].isdigit() and int(map_data[nr][nc]) == height + 1:
                    queue.append((nr, nc, height + 1))

    return len(reachable_nines)


def find_rating(map_data, start):
    """Calculate the rating for a single trailhead."""
    rows, cols = len(map_data), len(map_data[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    visited = set()
    unique_trails = set()

    def dfs(r, c, path):
        # If out of bounds or already visited, stop
        if not (0 <= r < rows and 0 <= c < cols):
            return

        # If not a digit or not part of an increasing path, stop
        if not map_data[r][c].isdigit() or int(map_data[r][c]) != len(path):
            return

        visited.add((r, c))
        path.append((r, c))

        # If we reach height 9, add this path to unique trails
        if map_data[r][c] == '9':
            unique_trails.add(tuple(path))
        else:
            # Explore neighbors
            for dr, dc in directions:
                dfs(r + dr, c + dc, path[:])

    dfs(start[0], start[1], [])
    return len(unique_trails)


def calculate_total_score_and_rating(map_data):
    """Calculate the total score and rating for all trailheads."""
    trailheads = find_trailheads(map_data)
    total_score = 0
    total_rating = 0

    for trailhead in trailheads:
        total_score += find_score(map_data, trailhead)
        total_rating += find_rating(map_data, trailhead)

    return total_score, total_rating


def main():
    map_file = "input.txt"
    map_data = read_map(map_file)
    total_score, total_rating = calculate_total_score_and_rating(map_data)
    print(f"Total Score: {total_score}")
    print(f"Total Rating: {total_rating}")


if __name__ == "__main__":
    main()
