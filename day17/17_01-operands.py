def combo_operand_value(operand, registers):
    """
    Calculates the value of a combo operand based on its type.
    """
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    elif operand == 7:
        raise ValueError("Combo operand 7 is reserved and invalid.")
    else:
        raise ValueError(f"Invalid combo operand: {operand}")

def run_program(registers, program):
    """
    Executes the 3-bit computer program given initial registers and program instructions.
    """
    output = []
    instruction_pointer = 0

    # Program execution loop
    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1] if instruction_pointer + 1 < len(program) else None

        if opcode == 0:  # adv: Division operation, stores in register A
            denominator = 2 ** combo_operand_value(operand, registers)
            if denominator == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            registers['A'] //= denominator

        elif opcode == 1:  # bxl: Bitwise XOR, stores result in register B
            registers['B'] ^= operand

        elif opcode == 2:  # bst: Combo operand modulo 8, stores in register B
            registers['B'] = combo_operand_value(operand, registers) % 8

        elif opcode == 3:  # jnz: Jump if A is not zero
            if registers['A'] != 0:
                instruction_pointer = operand
                continue  # Skip increment of instruction_pointer

        elif opcode == 4:  # bxc: Bitwise XOR of registers B and C, stores in B
            registers['B'] ^= registers['C']

        elif opcode == 5:  # out: Combo operand modulo 8, output
            value = combo_operand_value(operand, registers) % 8
            output.append(value)

        elif opcode == 6:  # bdv: Division operation, stores in register B
            denominator = 2 ** combo_operand_value(operand, registers)
            if denominator == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            registers['B'] = registers['A'] // denominator

        elif opcode == 7:  # cdv: Division operation, stores in register C
            denominator = 2 ** combo_operand_value(operand, registers)
            if denominator == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            registers['C'] = registers['A'] // denominator

        else:
            raise ValueError(f"Invalid opcode: {opcode}")

        # Move to the next instruction
        instruction_pointer += 2

    return output, registers

def read_input_file(file_path):
    """
    Reads input from a file and returns the initial register values and program instructions.
    """
    registers = {'A': 0, 'B': 0, 'C': 0}
    program = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Register A:"):
                registers['A'] = int(line.split(":")[1].strip())
            elif line.startswith("Register B:"):
                registers['B'] = int(line.split(":")[1].strip())
            elif line.startswith("Register C:"):
                registers['C'] = int(line.split(":")[1].strip())
            elif line.startswith("Program:"):
                program = [int(x.strip()) for x in line.split(":")[1].strip().split(",")]
    
    return registers, program

def main():
    # File path for input file
    input_file = "input.txt"

    # Read input file
    registers, program = read_input_file(input_file)

    # Run the program
    try:
        output, final_registers = run_program(registers, program)
        print("Output:", ",".join(map(str, output)))
        print("Final Registers:", final_registers)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
