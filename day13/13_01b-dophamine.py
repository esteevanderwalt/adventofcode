import math


def get_input_as_list(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().split() for line in f.readlines()]


def parse_input(input_data):
    games = []
    cur_game = {}
    for row in input_data:
        if len(row) == 0:
            continue
        if row[0] == "Button":
            cur_game[row[1].replace(":", "")] = (int(row[2].replace("X+", "").replace(",", "")), int(row[3].replace("Y+", "")))
        else:
            cur_game["prize"] = (int(row[1].replace("X=", "").replace(",", "")), int(row[2].replace("Y=", "")))
            games.append(cur_game)
            cur_game = {}
    return games


if __name__ == "__main__":
    input_data = get_input_as_list("input.txt")
    games = parse_input(input_data)
    max_times = 100
    prize_solutions = []
    higher_prize_solutions = []
    for game in games:
        AX = game['A'][0]
        BX = game['B'][0]
        prizeX = game['prize'][0]
        higherPriceX = game['prize'][0] + 10000000000000
        AY = game['A'][1]
        BY = game['B'][1]
        prizeY = game['prize'][1]
        higherPriceY = game['prize'][1] + 10000000000000
        xGCD = math.gcd(AX, BX)
        yGCD = math.gcd(AY, BY)
        a = round((prizeY - ((BY * prizeX) / BX)) / (AY - ((BY * AX) / BX)))
        b = round((prizeX - AX * a) / BX)
        if AX * a + BX * b == prizeX and AY * a + BY * b == prizeY:
            prize_solutions.append((a, b))
        a = round((higherPriceY - ((BY * higherPriceX) / BX)) / (AY - ((BY * AX) / BX)))
        b = round((higherPriceX - AX * a) / BX)
        if AX * a + BX * b == higherPriceX and AY * a + BY * b == higherPriceY:
            higher_prize_solutions.append((a, b))
    print(sum([sol[0] * 3 + sol[1] for sol in prize_solutions])) # part 1
    print(sum([sol[0] * 3 + sol[1] for sol in higher_prize_solutions])) # part 2
    