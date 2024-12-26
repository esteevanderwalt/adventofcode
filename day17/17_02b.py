import _utils as u
import sys

def get_combo_opr(reg, opr):
    if opr in [0,1,2,3]:
        return opr
    if opr == 4:
        return reg[0]
    if opr == 5:
        return reg[1]
    if opr == 6:
        return reg[2]
    if opr == 7:
        sys.exit("Combo operand 7 not valid!")

def parse_instruction(reg, opc, opr, out, ptr):
    if opc == 0:
        reg[0] = int(reg[0] / 2**get_combo_opr(reg, opr))
    elif opc == 1:
        reg[1] = reg[1] ^ opr
    elif opc == 2:
        reg[1] = get_combo_opr(reg, opr) % 8
    elif opc == 3:
        if reg[0] != 0:
            return reg, out, opr
    elif opc == 4:
        reg[1] = reg[1] ^ reg[2]
    elif opc == 5:
        out.append(get_combo_opr(reg, opr) % 8)
    elif opc == 6:
        reg[1] = int(reg[0] / 2**get_combo_opr(reg, opr))
    elif opc == 7:
        reg[2] = int(reg[0] / 2**get_combo_opr(reg, opr))
    return reg, out, ptr+2

lines = u.read_lines("input.txt")

regA = int(lines[0][12:])
regB = int(lines[1][12:])
regC = int(lines[2][12:])
reg = [regA, regB, regC]

program = [int(a) for a in lines[4][9:].split(",")]

#Q1

ptr = 0
out = []
while ptr < len(program):
    opc = program[ptr]
    opr = program[ptr+1]
    reg, out, ptr = parse_instruction(reg, opc, opr, out, ptr)

res = ""
for a in out:
    res += str(a)+","
print("Q1 answer:", res[:-1])

#Q2

possibleAs = [0]

for res in program[::-1]:
    newAs = []
    for ind in range(len(possibleAs)):
        regA = possibleAs[ind]
        updatedA = False
        for i in range(8):
            a = 8 * regA + i
            for b in range(8):
                if a % 8 == b:
                    if (b ^ int(a / 2**(b ^ 7))) % 8 == res:
                        updatedA = True
                        newAs.append(a)
    possibleAs = [a for a in newAs if a > 0]
    if len(possibleAs) == 0:
        print("Terminating: no valid values for regA left")
        break

possibleAs.sort()
print("Q2 answer(s):", possibleAs)