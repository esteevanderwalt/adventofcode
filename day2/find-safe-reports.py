# You receive a file where each line represents a report with levels in that line seperated by spaces
# Figure out which reports are safe
# * The levels are either all increasing or all decreasing.
# * Any two adjacent levels differ by at least one and at most three.

# Step 1 - read values from input.txt into a list
with open('input.txt', 'r') as f:
    lines = f.readlines()
reports = []
for line in lines:
    reports.append(list(map(int, line.split())))

# Step 2 - check if the reports are safe
safe_reports = []
for report in reports:
    is_safe = True
    increasing = None
    
    for i in range(1, len(report)):
        # Check if any two adjacent levels differ by at least one and at most three
        if not (1 <= abs(report[i] - report[i-1]) <= 3):
            is_safe = False
            break

        # Determine if the sequence is increasing or decreasing
        if report[i] > report[i-1]:
            if increasing is None:
                increasing = True  # Set direction as increasing
            elif increasing is False:  # Sequence flips to decreasing
                is_safe = False
                break
        elif report[i] < report[i-1]:
            if increasing is None:
                increasing = False  # Set direction as decreasing
            elif increasing is True:  # Sequence flips to increasing
                is_safe = False
                break

    if is_safe:
        safe_reports.append(report)

# Step 3 - print the safe reports
print(len(safe_reports))