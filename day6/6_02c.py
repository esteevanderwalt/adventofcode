import sys

file_name = 'input.txt'

directions = [(-1,0),(0,1),(1,0),(0,-1)]
direction_index = 0

def build_grid(file_name):
    with open(file_name) as file:
        cur = (-1,-1)
        grid = {}
        
        for y, row in enumerate(file):
            row = row.strip()
            for x, el in enumerate(row):
                if el == ".":
                    grid[(y,x)] = 0
                elif el == "#":
                    grid[(y,x)] = -1
                else:
                    grid[(y,x)] = 1
                    cur = (y,x)
    return grid,cur

def calc_next_pos(grid, cur, direction_index):
    new_pos = cur[0] + directions[direction_index][0], cur[1] + directions[direction_index][1]
    if new_pos not in grid:
        return False, False
    elif grid[new_pos] == -1:
        direction_index = (direction_index + 1) % len(directions)
        return(calc_next_pos(grid, cur, direction_index))
    else:
        return new_pos, direction_index

def main(direction_index):
    grid,cur = build_grid(file_name)
    visited_1 = 1

    visited = []

    on_grid = True
    while on_grid:
        new_pos, direction_index = calc_next_pos(grid, cur, direction_index)
    
        if not new_pos:
            on_grid = False
            break
        else:
            if grid[new_pos] == 0:
                visited_1 += 1
                visited.append(new_pos)
                grid[new_pos] = 1
            cur = new_pos
    print(f'Part 1 Visited {visited_1} cells')

    
    loop_2 = 0
    for i,pos in enumerate(visited):
        grid,cur = build_grid(file_name)
        grid[pos] = -1
        is_loop = False
        on_grid = True
        direction_index = 0
        loop_visited = []
        index = 0
        max = len(grid.keys()) + 1
        while on_grid:
            new_pos, direction_index = calc_next_pos(grid, cur, direction_index)
            index += 1
    
            if not new_pos:
                on_grid = False
                break
            elif index > max:
                loop_2 += 1
                on_grid = False
                break
            else:
                if grid[new_pos] == 0:
                    loop_visited.append(new_pos)
                    grid[new_pos] = 1
                                        
                cur = new_pos
        if is_loop:
            loop_2 += 1
        grid[pos] = 0
    
                
                        
    print('Part 2: The total number of loops is ' + str(loop_2))


main(direction_index)