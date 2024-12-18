import heapq

def parse_input(data):
    bytes = []
    for line in data:
        num_str = line.split(',')
        x = int(num_str[1])
        y = int(num_str[0])
        bytes.append((x,y))
    return bytes


def is_valid_move(curr, corrupted, size_space):
    currx, curry = curr
    if 0 <= currx < size_space and 0 <= curry < size_space and curr not in corrupted:
        return True
    return False


def print_map(corrupted, size_space):
    for i in range(size_space):
        for j in range(size_space):
            if (i,j) in corrupted:
                print('#', end='')
            else:
                print('.', end='')
        print()


def dijkstra(corrupted, size_space):
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]
    max_int = size_space * size_space + 1
    mindist = [[max_int for _ in range(size_space)] for _ in range(size_space)]
    mindist[0][0] = 0
    pq = []
    visited = set()
    in_heap = set()

    heapq.heappush(pq, (0, 0, 0))
    in_heap.add((0, 0, 0))

    while pq:
        dist, r, c = heapq.heappop(pq)
        visited.add((r,c))
        # print(dist, r, c)
        mindist[r][c] = min(mindist[r][c], dist)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (nr, nc) in visited:
                continue
            if nr == size_space - 1 and nc == size_space - 1:
                return dist + 1
            if is_valid_move((nr, nc), corrupted, size_space) and (dist+1, nr, nc) not in in_heap:
                heapq.heappush(pq, (dist + 1, nr, nc))
                in_heap.add((dist+1, nr, nc))
    return mindist[size_space-1][size_space-1]


def part1(bytes):
    size_space = 71
    corrupted = set()
    for i in range(1024):
        corrupted.add(bytes[i])
    # print_map(corrupted, size_space)
    print("Part 1:")
    print(dijkstra(corrupted, size_space))
    

# Takes a while to run
def part2_linearsearch(bytes):
    print('Part 2:')
    size_space = 71
    corrupted = set()
    for i in range(len(bytes)):
        # print(f"Added byte {i}")
        corrupted.add(bytes[i])
        last_dist = dijkstra(corrupted, size_space)
        if last_dist == size_space * size_space + 1:
            y, x = bytes[i]
            # print(i)
            print(f"{x},{y}")
            break


# Runs pretty quickly
def part2_binarysearch(bytes):
    print('Part 2:')
    size_space = 71
    hi = len(bytes)
    lo = 0
    while lo < hi:
        mid = (lo+hi)//2
        # print(lo, mid, hi)
        corrupted = set(bytes[:mid])
        last_dist = dijkstra(corrupted, size_space)
        if last_dist == size_space * size_space + 1:
            hi = mid - 1
        else:
            lo = mid + 1
    y, x = bytes[mid]
    print(f"{x},{y}")


if __name__=="__main__":
    print("\n--- Day 18: RAM Run ---")
    file = open("input.txt","r")
    data = [x.strip() for x in file.readlines()]
    bytes = parse_input(data)
    part1(bytes)
    part2_binarysearch(bytes)
    print()