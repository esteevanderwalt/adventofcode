# You need to write a script that will multiply all the valid multiply instructions,
# add the results together and print the final result
# The input is corrupted though and valid multiply instructions are on in the following format mul(d{1,3},d{1,3})
# All invalid characters inbetween should be ignored

# There are two new instructions you'll need to handle:
# The do() instruction enables future mul instructions.
# The don't() instruction disables future mul instructions.
# Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

import re

# Step 1 - Read values from input.txt
with open('input.txt', 'r') as f:
    content = f.read()

# Step 2 - Define regex for valid instructions and control instructions
valid_regex = r'.*?mul\((\d{1,3}),(\d{1,3})\)'  # mul(d{1,3},d{1,3})
do_regex = r'.*?do\(\)'  # do() enables mul()
dont_regex = r'.*?don\'t\(\)'  # don't() disables mul()

# Step 3 - Initialize variables
total_sum = 0
is_enabled = True  # Initial state: mul() instructions are enabled

# Step 4 - Process the content
instructions = re.split(r'(do\(\)|don\'t\(\))', content)  # Split on 'do()' and 'don't()'

for instruction in instructions:
    # If it's a 'do' instruction, enable mul()
    if re.match(do_regex, instruction):
        is_enabled = True
    # If it's a 'don't' instruction, disable mul()
    elif re.match(dont_regex, instruction):
        is_enabled = False
    # If it's a valid mul() instruction and mul is enabled, process it
    elif re.match(valid_regex, instruction):
        if is_enabled:
            matches = re.findall(valid_regex, instruction)
            if matches:
                total_sum += sum(int(num1) * int(num2) for num1, num2 in matches)

# Step 5 - Output the final result
print(f"{total_sum}")