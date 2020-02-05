import csv
import os
from sys import argv
from game_runner import run_tests

num_of_teams = int(argv[1])
max_games_left = int(argv[2])
num_of_constraints = int(argv[3])

os.system('python3 create_test_files.py %d %d %d' %
          (num_of_teams, max_games_left, num_of_constraints))

output = run_tests(max_games_left, num_of_teams)

# print('output')
# print(output)
os.system('pwd')
os.chdir('../..')
file_name = 'CSV_files/Runtimes.csv'
header = ['Constraints', 'time1', 'time2', 'time3', 'time4', 'time5', 'time6',
          'time7', 'time8', 'time9', 'time10']
new_header = ['number_of_teams', 'fixtures_left', 'number_of_constraints',
              'runtime']

with open(file_name, 'a', newline='') as file:
    writer = csv.writer(file)

    # write headers to csv file
    if os.stat(file_name).st_size == 0:
        writer.writerow(new_header)

    writer.writerows(output)
