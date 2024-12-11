# Your task is the take the string of inputs
# Each uneven position indicates how many blocks a file consists of and each even position indicates the blocks between the files.
# You need to compact the drive by removing the spaces between the files starting by the shifting the last block of a file to the first open space 

# Each file has an id where ids start from 0
# The final result should be the sum of (the id * block number) for the whole drive

def read_file(file_name) -> list:
    with open(file_name, "r") as file:
        result = list(map(int, file.read().strip()))
    return result


# Step 1: Read of the values
inputs = read_file("input.txt")
files_blocks = [inputs[i] for i in range(0, len(inputs), 2)]
space_blocks = [inputs[i] for i in range(1, len(inputs), 2)]

# print(files_blocks)
# print(space_blocks)

# Step 2: Compact the drive
drive = []
current = 0
files_end = len(files_blocks) - 1
while current <= files_end:
    # Add the current file blocks to the drive
    for _ in range(files_blocks[current]):
        drive.append(current)

    # Fill spaces between files
    while space_blocks[current] > 0:
        if files_end < 0:  # No more files to move
            break

        # Move a block from the last file to fill the space
        drive.append(files_end)
        files_blocks[files_end] -= 1
        space_blocks[current] -= 1

        # If the last file is empty, move to the previous file
        while files_end >= 0 and files_blocks[files_end] <= 0:
            files_end -= 1

    current += 1

# Step 3: Calculate the result
result = sum(i * drive[i] for i in range(len(drive)))
print(result)
