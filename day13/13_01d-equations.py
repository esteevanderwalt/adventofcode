import re


def read_input_13(filename):
    f = open(filename)
    arcades = []
    for l  in f.read().split("\n\n"):
        v = [int(d) for d in re.findall(r"\d+",l)]
        A = v[0]+1j*v[1]
        B = v[2]+1j*v[3]
        P = v[4]+1j*v[5]
        arcades.append([A,B,P])
    return arcades


def find_chapest_win_bruteforce(arcade):
    A,B,P = arcade
    Pmax = 100*A+100*B
    if Pmax.real<P.real or Pmax.imag<P.imag:
        return -1
    else:
        wins = []
        for na in range(0,101):
            a = na*A
            dP = (P-a)
            if dP.real%B.real==0 and dP.imag%B.imag==0:
                nb = int(dP.real//B.real)
                if nb>100:
                    continue
                if nb == dP.imag//B.imag:
                    wins.append((na,nb))
                else:
                    continue
        if len(wins):
            return min([3*na+nb for na,nb in wins ])
        else:
            return -1
        

def part1(filename):
    arcades = read_input_13(filename)
    tokens = 0
    for arcade in arcades:
        t = find_chapest_win_bruteforce(arcade)
        if t>0:
            tokens+=t
    return tokens


print("Test 1:",part1("input_test.txt"))
print("Part 1:",part1("input.txt"))


from sympy import solve
from sympy.abc import x, y


def find_chapest_win_fast(arcade):
    # solve as a system of 2 linear equations
    A,B,P = arcade
    Ar,Ai = int(A.real),int(A.imag)
    Br,Bi = int(B.real),int(B.imag)
    Pr,Pi = int(P.real),int(P.imag)
    sol = solve([Ar*x + Br*y -Pr, Ai*x + Bi*y - Pi], [x, y])
    if int(sol[x])==sol[x] and int(sol[y])==sol[y]: # integer solutions (assuming there's only one)        
        return 3*int(sol[x]) + int(sol[y])
    return -1


def part1_fast(filename):
    arcades = read_input_13(filename)
    tokens = 0
    for arcade in arcades:
        t = find_chapest_win_fast(arcade)
        if t>0:
            tokens+=t
    return tokens


print("Test 1:",part1_fast("input_test.txt"))
print("Part 1:",part1_fast("input.txt"))


def part2(filename):
    arcades = read_input_13(filename)
    tokens = 0
    for arcade in arcades:
        arcade[2] += 10000000000000 + 10000000000000j
        t = find_chapest_win_fast(arcade)
        if t>0:
            tokens+=t
    return tokens


print("Test 2:",part2("input_test.txt"))
print("Part 2:",part2("input.txt"))