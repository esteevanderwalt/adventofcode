import utils
from collections import deque

inp, MAX, P1 = utils.get_input(18), 70, 1024
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))

corrupted = []
rows = inp.strip().split("\n")
grid = set((i, j) for i in range(MAX + 1) for j in range(MAX + 1))
for i, row in enumerate(rows):
    x, y = map(int, row.split(",", maxsplit=1))
    corrupted.append((x, y))
spos, epos = (0, 0), (MAX, MAX)

def traverse(grid, spos, epos, corrupted, ccount):
    grid_ = grid - set(corrupted[:ccount + 1])
    Q = deque([spos])
    steps = {spos: 0}
    while Q:
        pos = Q.popleft()
        if pos == epos:
            break
        for d in DIRS:
            pos_ = pos[0] + d[0], pos[1] + d[1]
            if pos_ not in grid_ or pos_ in steps:
                continue
            steps[pos_] = steps[pos] + 1
            Q.append(pos_)
    return steps

steps_p1 = traverse(grid, spos, epos, corrupted, P1)
assert epos in steps_p1
utils.write_output(steps_p1[epos], day=18, w=1)

# Just do binary search lmao
bmin, bmax = P1, len(corrupted) 
while bmax - bmin >= 4:
    m = (bmin + bmax) // 2
    steps_m = traverse(grid, spos, epos, corrupted, m)
    if epos in steps_m:
        bmin = m + 1
    else:
        bmax = m
for m in range(bmin, bmax + 1):
    steps_m = traverse(grid, spos, epos, corrupted, m)
    if epos not in steps_m:
        x, y = corrupted[m]
        utils.write_output(f"{x},{y}", day=18, a=1)
        break
