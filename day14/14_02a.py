import re
import math
import matplotlib.pyplot as plt
import argparse
import os

filename = "input.txt"
height, width = 103, 101
rows = []

parser = argparse.ArgumentParser()
parser.add_argument(
    "--mode",
    choices={"exploratory", "threshold"},
    default="threshold",
    help="exploratory: plot the ratio.\n\
                threshold: find all the plots for which the ratio is below a threshold and store them.",
)

args = parser.parse_args()
os.makedirs("./output", exist_ok=True)


def compute_steps(rows, seconds):
    quadrants = [0, 0, 0, 0]
    xs = []
    ys = []
    for row in rows:
        x, y, vx, vy = [int(num) for num in re.findall(r"(-?\d+)", row)]
        final_x = (vx * seconds + x) % width
        final_y = (vy * seconds + y) % height
        xs.append(final_x)
        ys.append(height - final_y)
        if final_x < width // 2 and final_y < height // 2:
            quadrants[0] += 1
        elif final_x > width // 2 and final_y < height // 2:
            quadrants[1] += 1
        elif final_x < width // 2 and final_y > height // 2:
            quadrants[2] += 1
        elif final_x > width // 2 and final_y > height // 2:
            quadrants[3] += 1
    return quadrants, xs, ys


with open(filename) as f:
    for row in f:
        rows.append(row)
quadrants, _, _ = compute_steps(rows, 100)
print("Part 1:", math.prod(quadrants))

if args.mode == "threshold":
    threshold = float(input("Insert threshold: "))
ratios = []
for seconds in range(100000):
    quadrants, xs, ys = compute_steps(rows, seconds)
    ratio = math.prod(quadrants)
    ratios.append(ratio)
    if args.mode == "threshold" and ratio < threshold:
        print("Seconds:", seconds)
        plt.figure()
        plt.scatter(xs, ys)
        plt.title(f"Seconds {seconds}")
        plt.savefig(f"./output/Seconds_{seconds}.jpg")
        plt.show()
        keep_going = str(input("Continue (Y/N)? "))
        if keep_going.capitalize() == "N":
            break
if args.mode == "exploratory":
    plt.figure()
    plt.plot(range(len(ratios)), ratios)
    plt.title("Ratio (output exploratory mode)")
    plt.savefig("./output/ratio_values.jpg")
    plt.show()


# Part 1: this was straightforward, I just computed the advances mod 101 and 103 and it worked.

# Part 2: I did this in two steps. First, I plotted the values for the safety factors over 100000 
# steps and I noticed there were sudden drops in the plot. Then, I established a threshold (1e8) 
# for the safety factor to explore only these values and each one of them turned out to be a Christmas tree.