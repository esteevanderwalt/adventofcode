from itertools import chain


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

def calc_prev(A_n_minus_k, o_n_minus_k):
    if A_n_minus_k == 0 and o_n_minus_k == 0:
        return [7]
    matches = []
    for A_n_minus_k_minus_1 in range(8 * A_n_minus_k, 8*A_n_minus_k + 8):
        out = run_program([A_n_minus_k_minus_1, 0, 0], program)[0]
        if out == o_n_minus_k:
            matches.append(A_n_minus_k_minus_1)
    return matches

def calc_first(program):
    # work backwards iteratively through the required outputs
    flattened = list(chain.from_iterable(program))
    A_ns = [[0]]
    for o_n in flattened[::-1]:
        A_n_minus_1 = []
        for A_n in A_ns[0]:
            matches = calc_prev(A_n, o_n)
            if len(matches) > 0:
                A_n_minus_1.extend(matches)
        A_ns.insert(0, A_n_minus_1)

    return A_ns[0][0]

# Main function
def main():
    filename = "input.txt"  # Replace with your input file name
    registers, program = read_input_file(filename)

    A_n_minus_k, o_n_minus_k = calc_first(program)
    result = calc_prev(A_n_minus_k, o_n_minus_k)
    print("The lowest positive initial value for Register A is:", result)

if __name__ == "__main__":
    main()
