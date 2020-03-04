import csv
import os
from sys import argv
from game_runner import run_tests
from csv_file_writer import write_csv_file

num_of_teams = int(argv[1])
num_of_constraints = int(argv[2])
csv_type = argv[3]

for i in range(6, num_of_teams+1):
    write_csv_file(i, i-2, num_of_constraints, csv_type)
