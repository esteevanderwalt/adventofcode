import itertools as it, functools as ft, re

games = [tuple(map(int, it.chain(*map(ft.partial(re.findall, r'\d+'), game)))) for game in it.batched(open('input.txt').read().splitlines(),4)]
for p, total in (0,0), (10000000000000, 0):
    for ax, ay, bx, by, X, Y in games:
        A = int(round(((X+p)-bx*(B:=int(round(((Y+p)-(ay*(X+p))/ax)/(by-(ay*bx)/ax), 0))))/ax, 0))
        total+=A*3+B if A*ax+B*bx==(X+p) and A*ay+B*by==(Y+p) else 0
    print(total)