# Challenge:
# 1. Take a list of locations as input. There are two values per line
# 2. Read the left values into list1 and the right value into list 2
# 3. Order each of the two lists
# 4. Find the distance between each pair of locations
# 5. Print the sum of the distances

# Step 1 and 2 - read values from input.txt into two lists
with open('input.txt', 'r') as f:
    lines = f.readlines()
list1 = []
list2 = []
for line in lines:
    values = line.split()
    list1.append(int(values[0]))
    list2.append(int(values[1]))

# Step 3 to 4 - order these lists and calculate the distance between each pair
list1.sort()
list2.sort()
distances = []
for i in range(len(list1)):
    distances.append(abs(list2[i] - list1[i]))

# Step 5 - print the sum of the distances
print(sum(distances))


