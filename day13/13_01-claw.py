import re
from math import inf, gcd
from collections import deque
from heapq import heappop, heappush


def can_reach(prize, button_a, button_b):
    """Checks if the prize position is reachable."""
    dx_gcd = gcd(button_a[0], button_b[0])
    dy_gcd = gcd(button_a[1], button_b[1])
    x_prize, y_prize = prize
    return x_prize % dx_gcd == 0 and y_prize % dy_gcd == 0


def parse_input(file_path):
    """Parses the input file to extract machine configurations."""
    machines = []
    with open(file_path, 'r') as f:
        data = f.read().strip().split("\n\n")
        for block in data:
            lines = block.split("\n")
            button_a = list(map(int, re.findall(r"X\+(\d+), Y\+(\d+)", lines[0])[0]))
            button_b = list(map(int, re.findall(r"X\+(\d+), Y\+(\d+)", lines[1])[0]))
            prize = list(map(int, re.findall(r"X=(\d+), Y=(\d+)", lines[2])[0]))
            machines.append({
                'a': button_a,  # [delta_x_a, delta_y_a]
                'b': button_b,  # [delta_x_b, delta_y_b]
                'prize': prize  # [x_prize, y_prize]
            })
    return machines


def minimum_tokens(machine):
    """Finds the minimum tokens required to win the prize for a single machine."""
    delta_x_a, delta_y_a = machine['a']
    delta_x_b, delta_y_b = machine['b']
    x_prize, y_prize = machine['prize']

    # Check if the prize is reachable
    if not can_reach(machine['prize'], machine['a'], machine['b']):
        return inf

    # BFS to find the minimum cost
    queue = deque([(0, 0, 0)])  # (m, n, cost)
    visited = set()

    count = 0
    while queue:
        m, n, cost = queue.popleft()
        print(m, n, cost)

        count += 1
        if count == 10:
            break

        # Calculate current claw position
        x = m * delta_x_a + n * delta_x_b
        y = m * delta_y_a + n * delta_y_b

        # Check if we reached the prize position
        if x == x_prize and y == y_prize:
            return cost

        # Avoid re-visiting states
        if (m, n) in visited:
            continue
        visited.add((m, n))

        # Dynamic larger steps towards the prize
        # Heuristically allow jumps proportional to the remaining distance
        for a_steps in range(1, 6):  # Try up to 5 presses of Button A
            for b_steps in range(1, 6):  # Try up to 5 presses of Button B
                new_m = m + a_steps
                new_n = n + b_steps
                new_cost = cost + (a_steps * 3) + (b_steps * 1)

                # Calculate new position
                new_x = new_m * delta_x_a + new_n * delta_x_b
                new_y = new_m * delta_y_a + new_n * delta_y_b

                # Add state if within bounds and not visited
                if new_x <= x_prize and new_y <= y_prize:
                    queue.append((new_m, new_n, new_cost))

        # Continue exploring incrementally
        queue.append((m + 1, n, cost + 3))  # Press Button A once
        queue.append((m, n + 1, cost + 1))  # Press Button B once

    return inf  # If no solution is found (shouldn't happen for valid inputs)


def main(file_path):
    """Main function to calculate the minimum tokens for all machines."""
    machines = parse_input(file_path)
    total_tokens = 0

    for i, machine in enumerate(machines):
        print(machine)
        tokens = minimum_tokens(machine)
        if tokens == inf:
            print(f"Machine {i + 1}: Cannot win the prize!")
        else:
            print(f"Machine {i + 1}: Minimum tokens = {tokens}")
            total_tokens += tokens
        break

    print(f"Total tokens required: {total_tokens}")


def main_parallel(file_path):
    machines = parse_input(file_path)
    total_tokens = 0

    with ThreadPoolExecutor() as executor:
        results = executor.map(minimum_tokens, machines)

    for i, tokens in enumerate(results):
        if tokens == inf:
            print(f"Machine {i + 1}: Cannot win the prize!")
        else:
            print(f"Machine {i + 1}: Minimum tokens = {tokens}")
            total_tokens += tokens

    print(f"Total tokens required: {total_tokens}")


if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file path
    main(input_file)
