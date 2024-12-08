# Your tasks is to take the input above.
# Each line represents a single equation
# The test value appears before the colon on each line; it is your job to determine whether 
# the remaining numbers can be combined with operators to produce the test value.

# Operators are always evaluated left-to-right, not according to precedence rules. 
# Furthermore, numbers in the equations cannot be rearranged. There are only two different types of operators: add (+) and multiply (*).

# Find all the equations that can be solved given the rules above. Take the result of these equations and add them up to provide a final result

from itertools import product


# Define a function to evaluate an equation with given operators
def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i in range(1, len(numbers)):
        if operators[i-1] == '+':
            result += numbers[i]
        elif operators[i-1] == '*':
            result *= numbers[i]
    return result


# Function to solve the equations based on input from the file
def solve_equations(file_path):
    total_sum = 0

    # Read equations from the file
    with open(file_path, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace and process each line
            line = line.strip()

            if not line:  # Skip empty lines
                continue

            # Split the line at the colon to separate test value and numbers
            test_value_str, numbers_str = line.split(':')
            test_value = int(test_value_str.strip())  # Convert test value to integer
            numbers = list(map(int, numbers_str.strip().split()))  # Convert numbers to a list of integers

            # Generate all possible operator combinations (+ and *)
            operator_combinations = product(['+', '*'], repeat=len(numbers) - 1)

            # Check each combination of operators
            for operators in operator_combinations:
                if evaluate_expression(numbers, operators) == test_value:
                    total_sum += test_value
                    break  # No need to check other operator combinations for this equation

    return total_sum


# Path to the input file
file_path = 'input.txt'

# Execute the function
result = solve_equations(file_path)
print(f"The final result is: {result}")
