# Challenge:
# 1. Take a list of locations as input. There are two values per line
# 2. Read the left values into list1 and the right value into list 2
# 3. Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list
# 4. Print the sum of the distances

# Step 1 and 2 - read values from input.txt into two lists
with open('input.txt', 'r') as f:
    lines = f.readlines()
list1 = []
list2 = []
for line in lines:
    values = line.split()
    list1.append(int(values[0]))
    list2.append(int(values[1]))

# Step 3 - calculate the similarity score
similarity_score = 0
for i in range(len(list1)):
    similarity_score += list1[i] * list2.count(list1[i])

# Step 4 - print the similarity score
print(similarity_score)