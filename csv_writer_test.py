import csv

row_list = [["Number of teams", "Number of games left", "Number of constraints", "Time"], [8, 20, 3, 0.13]]

with open('CSV_files/test_csv.csv', 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerows(row_list)
