# You get a list of ordering rules in the format X|Y. This indicates that X should exist in the output before Y.
# You get a second list of numbers with all the numbers that should be printed. This list should follow the ordering rules.

# the input you receive first contains the list of rules, one rule per line
# there will then be a blank line
# then the list of number will follow to be printed given the rules. each line will contain a new set of numbers that should follow the rules

# for the output, determine which set of numbers adhere to the rules
# for those sets that adhere, find the middle number
# and lastly add all the middle numbers together and print the sum

def parse_input(input_text):
    """Parses the input into rules and sets of numbers."""
    parts = input_text.strip().split("\n\n")
    rules = [rule.strip() for rule in parts[0].split("\n") if rule.strip()]
    number_sets = [[int(num) for num in line.split(',')] for line in parts[1].split("\n") if line.strip()]
    return rules, number_sets


def check_rule_compliance(rules, number_set):
    """Checks if a set of numbers adheres to the given ordering rules."""
    index_map = {num: i for i, num in enumerate(number_set)}
    for rule in rules:
        x, y = rule.split('|')
        x, y = int(x), int(y)
        # if either number is not in the set, the rule is invalid and can be ignored
        if x not in index_map or y not in index_map:
            continue
        # valid rule so lets validate
        if index_map.get(x, float('inf')) >= index_map.get(y, float('inf')):
            return False
    return True


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
        # if the set adheres to the rules, find the middle number and add it to the total sum
        if check_rule_compliance(rules, number_set):
            middle_number = find_middle_number(number_set)
            total_sum += middle_number

    print(total_sum)


# Example usage
# Replace 'input.txt' with the path to your input file
do_the_work('input.txt')
