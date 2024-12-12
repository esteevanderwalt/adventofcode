# You are given a map of a garden 
# Each garden plot grows only a single type of plant and is indicated by a single letter on your map.
# When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), 
# they form a region. 
# The area of a region is simply the number of garden plots the region contains.

# Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of 
# garden plots in the region that do not touch another garden plot in the same region.

# Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions.

# Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. 
#     The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

# Step1: Read the map from the file and return it as a list of lists.
# Step2: Find all the regions on the map 
# Step3: For each region, calculate the area and perimeter
# Step4: Calculate the price of fence for each region by multiplying the area by the perimeter
# Step5: Print the total price of fencing for the map by summing the price of fence for each region.

# Extension: Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. 
# Each straight section of fence counts as a side, regardless of how long it is.

def get_map(file_path):
    # Read garden map from the file
    with open(file_path, 'r') as f:
        garden_map = [list(line.strip()) for line in f.readlines()]
    return garden_map


def calculate_fencing_cost(garden_map, use_bulk_discount=False):
    rows, cols = len(garden_map), len(garden_map[0])
    visited = [[False] * cols for _ in range(rows)]

    def flood_fill(r, c, plant_type):
        """Flood fill to calculate area, perimeter, and sides of a region."""
        stack = [(r, c)]
        area = 0
        perimeter = 0
        boundary_cells = []

        while stack:
            x, y = stack.pop()
            if visited[x][y]:
                continue
            visited[x][y] = True
            area += 1

            # Check all four neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if garden_map[nx][ny] == plant_type and not visited[nx][ny]:
                        stack.append((nx, ny))
                    elif garden_map[nx][ny] != plant_type:
                        perimeter += 1
                else:
                    perimeter += 1

            # Record boundary cells for side calculation
            boundary_cells.append((x, y))

        # Calculate sides using boundary cells
        horizontal_sides = set()
        vertical_sides = set()

        # Detect horizontal sides
        print(boundary_cells)
        for row in range(rows):
            start = None
            for col in range(cols):
                if (row, col) in boundary_cells and (col == 0 or (row, col-1) not in boundary_cells):
                    start = col  # Start of a new horizontal segment
                if start is not None and ((col == cols-1) or ((row, col+1) not in boundary_cells)):
                    # End of the horizontal segment
                    horizontal_sides.add((row, start, col))
                    start = None

        # Detect vertical sides
        for col in range(cols):
            start = None
            for row in range(rows):
                if (row, col) in boundary_cells and (row == 0 or (row-1, col) not in boundary_cells):
                    start = row  # Start of a new vertical segment
                if start is not None and ((row == rows-1) or ((row+1, col) not in boundary_cells)):
                    # End of the vertical segment
                    vertical_sides.add((start, row, col))
                    start = None

        total_sides = len(horizontal_sides) + len(vertical_sides)
        print(f"Region: {plant_type}, Area: {area}, Perimeter: {perimeter}, Sides: {total_sides}")
        return area, perimeter, total_sides

    total_cost = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:  # Start a new region
                area, perimeter, sides = flood_fill(r, c, garden_map[r][c])
                if use_bulk_discount:
                    total_cost += area * sides
                else:
                    total_cost += area * perimeter

    return total_cost


# Example Usage
garden_map = get_map("input_test3.txt")
use_bulk_discount = True  # Toggle this to apply the bulk discount
result = calculate_fencing_cost(garden_map, use_bulk_discount)
print(f"Total fencing cost: {result}")
