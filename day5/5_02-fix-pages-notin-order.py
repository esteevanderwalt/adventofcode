# You get a list of ordering rules in the format X|Y. This indicates that X should exist in the output before Y.
# You get a second list of numbers with all the numbers that should be printed. This list should follow the ordering rules.

# the input you receive first contains the list of rules, one rule per line
# there will then be a blank line
# then the list of number will follow to be printed given the rules. each line will contain a new set of numbers that should follow the rules

# for the output, determine which set of numbers does not adhere to the rules
# fix these using the rules
# find the middle number
# and lastly add all the middle numbers together and print the sum

def parse_input(input_text):
    """Parses the input into rules and sets of numbers."""
    parts = input_text.strip().split("\n\n")
    rules = [rule.strip() for rule in parts[0].split("\n") if rule.strip()]
    number_sets = [[int(num) for num in line.split(',')] for line in parts[1].split("\n") if line.strip()]
    return rules, number_sets


def is_compliant(rules, number_set):
    """Checks if the number_set complies with all rules."""
    index_map = {num: i for i, num in enumerate(number_set)}
    for rule in rules:
        x, y = rule.split('|')
        x, y = int(x), int(y)
        if x in index_map and y in index_map:
            if index_map[x] >= index_map[y]:
                return False
    return True


def fix_rule_compliance(rules, number_set):
    """Ensures that a set of numbers adheres to all the given ordering rules."""
    while not is_compliant(rules, number_set):
        # Try to fix the order by applying the rules iteratively
        index_map = {num: i for i, num in enumerate(number_set)}
        for rule in rules:
            x, y = rule.split('|')
            x, y = int(x), int(y)
            if x in index_map and y in index_map:
                if index_map[x] >= index_map[y]:
                    # Fix the issue by placing x before y
                    x_index = index_map[x]
                    y_index = index_map[y]
                    if x_index > y_index:
                        # Swap x and y to enforce the rule
                        number_set[x_index], number_set[y_index] = number_set[y_index], number_set[x_index]
                    # Update index_map after fixing
                    index_map = {num: i for i, num in enumerate(number_set)}
    return number_set


def find_middle_number(number_set):
    """Finds the middle number of a set."""
    middle_index = len(number_set) // 2
    return number_set[middle_index]


def do_the_work(file_path):
    with open(file_path, 'r') as file:
        input_text = file.read()

    # parse the input
    rules, number_sets = parse_input(input_text)
    total_sum = 0

    # check each number set for rule compliance
    for number_set in number_sets:
        # if the set does not adhere to the rules, fix it, find the middle number and add it to the total sum
        if not is_compliant(rules, number_set):
            fixed_number_set = fix_rule_compliance(rules, number_set)
            middle_number = find_middle_number(fixed_number_set)
            total_sum += middle_number

    print(total_sum)


# Example usage
# Replace 'input.txt' with the path to your input file
do_the_work('input.txt')
