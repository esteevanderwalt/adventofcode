# You need to write a script that will multiply all the valid multiply instructions,
# add the results together and print the final result
# The input is corrupted though and valid multiply instructions are on in the following format mul(d{1,3},d{1,3})
# All invalid characters inbetween should be ignored
import re

# Step 1 - Define regex for valid multiply instructions
valid_regex = r'mul\((\d{1,3}),(\d{1,3})\)'

# Step 2 - Read and process the file in one go
with open('input.txt', 'r') as f:
    content = f.read()  # Read the entire file as a single string

# Step 3 - Use re.findall to extract all matches
matches = re.findall(valid_regex, content)

# Step 4 - Compute the total sum of all valid instructions
total_sum = sum(int(num1) * int(num2) for num1, num2 in matches)


# Step 4 - Print the final result
print(total_sum)