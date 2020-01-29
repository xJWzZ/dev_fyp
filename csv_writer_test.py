import csv

with open('test_csv.csv', 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Number of teams", "Number of games left", "Number of constraints", "Time"])
    writer.writerow(["8", "20", "3", "0.13"])
