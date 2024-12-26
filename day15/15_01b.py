# display layout for debugging
def display_grid():
    for r in range(rows):
        for c in range(cols):
            if robot == (r,c):
                print('@', end='')
            elif (r,c) in walls:
                print('#', end= '')
            elif (r,c) in boxes:
                print('O', end='')
            else:
                print('.', end='')
        print('')
    print('')


with open('input.txt', 'r') as f:
    map, moves = f.read().split('\n\n')

# read in the initial status of the warehouse
map_lines = map.split('\n')
rows = len(map_lines)
cols = len(map_lines[0])
walls = set()
boxes = set()
for i, L in enumerate(map_lines):
    for j, c in enumerate(L):
        if c == '#':
            walls.add((i,j))
        elif c == 'O':
            boxes.add((i,j))
        elif c == '@':
            robot = (i,j)


# read in the moves made by the robot
move_lines = moves.split('\n')
for L in move_lines:
    for c in L:
        if c == '^':
            # build a list of robots and boxes that lie in a line
            # topmost object will be at front of list
            chain = [robot]
            i = robot[0]
            j = robot[1]
            i -= 1
            while (i,j) in boxes:
                chain.insert(0, (i,j))
                i -= 1
            # move chain of objects upward one space if possible
            if not (i,j) in walls:
                for b in chain[:-1]:
                    boxes.remove(b)
                    boxes.add((b[0] - 1, b[1]))
                robot = (robot[0] - 1, robot[1])

        elif c == '>':
            # build a list of robots and boxes that lie in a line
            # rightmost object will be at front of list
            chain = [robot]
            i = robot[0]
            j = robot[1]
            j += 1
            while (i,j) in boxes:
                chain.insert(0, (i,j))
                j += 1
            # move chain of objects rightward one space if possible
            if not (i,j) in walls:
                for b in chain[:-1]:
                    boxes.remove(b)
                    boxes.add((b[0], b[1] + 1))
                robot = (robot[0], robot[1] + 1)

            # display_grid()

        elif c == 'v':
            # display_grid()
            # build a list of robots and boxes that lie in a line
            # bottommost object will be at front of list
            chain = [robot]
            i = robot[0]
            j = robot[1]
            i += 1
            while (i,j) in boxes:
                chain.insert(0, (i,j))
                i += 1
            # move chain of objects downward one space if possible
            if not (i,j) in walls:
                for b in chain[:-1]:
                    boxes.remove(b)
                    boxes.add((b[0] + 1, b[1]))
                robot = (robot[0] + 1, robot[1])

        else:       # c == '<'
            # build a list of robots and boxes that lie in a line
            # leftmost object will be at front of list
            chain = [robot]
            i = robot[0]
            j = robot[1]
            j -= 1
            while (i,j) in boxes:
                chain.insert(0, (i,j))
                j -= 1
            # move chain of objects leftward one space if possible
            if not (i,j) in walls:
                for b in chain[:-1]:
                    boxes.remove(b)
                    boxes.add((b[0], b[1] - 1))
                robot = (robot[0], robot[1] - 1)


# calculate GPS sum 
total = 0
for b in boxes:
    total += 100 * b[0] + b[1]
print(total)