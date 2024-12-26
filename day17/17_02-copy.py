# Read input data
def read_input_file(filename):
    with open(filename, 'r') as file:
        registers = {}
        program = []
        for line in file:
            line = line.strip()
            if line.startswith("Register"):
                key, value = line.split(":")
                registers[key.strip()] = int(value.strip())
            elif line.startswith("Program"):
                program = list(map(int, line.split(":")[1].strip().split(",")))
        return registers, program

# Execute the program
def run_program(registers, program, initial_A):
    registers['Register A'] = initial_A
    registers['Register B'] = 0
    registers['Register C'] = 0
    instruction_pointer = 0
    output = []

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1] if instruction_pointer + 1 < len(program) else None

        if opcode == 0:  # adv
            denominator = 2 ** operand if operand <= 3 else 2 ** registers['Register ' + 'ABC'[operand - 4]]
            registers['Register A'] //= denominator
        elif opcode == 1:  # bxl
            registers['Register B'] ^= operand
        elif opcode == 2:  # bst
            value = operand if operand <= 3 else registers['Register ' + 'ABC'[operand - 4]]
            registers['Register B'] = value % 8
        elif opcode == 3:  # jnz
            if registers['Register A'] != 0:
                instruction_pointer = operand
                continue
        elif opcode == 4:  # bxc
            registers['Register B'] ^= registers['Register C']
        elif opcode == 5:  # out
            value = operand if operand <= 3 else registers['Register ' + 'ABC'[operand - 4]]
            output.append(value % 8)
        elif opcode == 6:  # bdv
            denominator = 2 ** operand if operand <= 3 else 2 ** registers['Register ' + 'ABC'[operand - 4]]
            registers['Register B'] = registers['Register A'] // denominator
        elif opcode == 7:  # cdv
            denominator = 2 ** operand if operand <= 3 else 2 ** registers['Register ' + 'ABC'[operand - 4]]
            registers['Register C'] = registers['Register A'] // denominator

        instruction_pointer += 2
    return output

# Find the lowest positive initial value for Register A
def find_lowest_initial_A(registers, program):
    target_output = "".join(map(str, program))  # The program itself as a string
    initial_A = 1

    while True:
        registers['Register A'] = initial_A
        output = run_program(registers, program, initial_A)
        registers['Register B'] = 0
        registers['Register C'] = 0
        output_str = "".join(map(str, output))

        if output_str == target_output:
            return initial_A
        initial_A += 1

def find_lowest_initial_A_memoized(registers, program):
    from functools import lru_cache

    # Target output to match
    target_output = "".join(map(str, program))

    # Memoization to cache previously tested values
    @lru_cache(None)
    def test_A_value(A):
        # Reset registers for each run
        registers_copy = registers.copy()
        registers_copy['Register A'] = A
        registers_copy['Register B'] = 0
        registers_copy['Register C'] = 0

        # Run the program and return the output as a string
        output = run_program(registers_copy, program, A)
        return "".join(map(str, output))

    # Start testing values of A
    A = 1
    while True:
        output = test_A_value(A)
        # print(f"Testing A={A}, Output={output[:20]}...")  # Debugging output

        if output == target_output and len(output) == len(target_output):
            return A  # Found the lowest valid value of A
        A += 1  # Increment A and test the next value

def find_lowest_initial_A_optimized(registers, program):
    def run_program_with_A(A):
        registers_copy = registers.copy()
        registers_copy['Register A'] = A
        registers_copy['Register B'] = 0
        registers_copy['Register C'] = 0
        return run_program(registers_copy, program, A)

    target_output = "".join(map(str, program))
    seen_states = {}  # To detect cycles: {hash of output: A value}

    A = 1
    while True:
        output = run_program_with_A(A)
        output_str = "".join(map(str, output))

        # Stop when output matches program
        if output_str == target_output and len(output_str) == len(target_output):
            return A

        # Check for cycles
        state_hash = hash(tuple(output))
        if state_hash in seen_states:
            print(f"Cycle detected at A={A}. Skipping redundant checks.")
            break

        # Save current state
        seen_states[state_hash] = A
        A += 1  # Increment A to test the next value

# Main function
def main():
    filename = "input.txt"  # Replace with your input file name
    registers, program = read_input_file(filename)
    
    lowest_A = find_lowest_initial_A(registers, program)
    print("The lowest positive initial value for Register A is:", lowest_A)

if __name__ == "__main__":
    main()
