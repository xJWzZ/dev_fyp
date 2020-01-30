import csv
import os
from sys import argv
from game_runner import run_tests

num_of_teams = int(argv[1])
max_games_left = int(argv[2])
num_of_constraints = int(argv[3])

os.system('python3 create_test_files.py %d %d %d' %
          (num_of_teams, max_games_left, num_of_constraints))

output = run_tests(max_games_left, 4)

# print('output')
# print(output)
os.system('pwd')
os.chdir('../..')

with open('CSV_files/%dNumTeams.csv' % num_of_teams, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)
