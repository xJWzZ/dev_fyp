import csv
import os
from game_runner import run_tests
from create_test_files import create_test_files

# num_of_teams = int(argv[1])
# max_games_left = int(argv[2])
# num_of_constraints = int(argv[3])

def write_csv_file(num_of_teams, max_games_left, num_of_constraints, csv_type):
    if max_games_left >= num_of_teams-1:
        print('Too many games left. Choose a lower number')
        exit()
    else:
        print(max_games_left, num_of_teams-1)
    # os.system('python3 create_test_files.py %d %d %d' %
    #           (num_of_teams, max_games_left, num_of_constraints))

    create_test_files(num_of_teams, max_games_left,
                      num_of_constraints)

    if csv_type == "fpoints":
        file_name = 'CSV_files/FpointsMin.csv'
    elif csv_type == "min_num_losses":
        file_name = 'CSV_files/MinNumLosses.csv'
    else:
        return "Error: not a valid CSV type. Choose fpoints or min_num_losses"

    [header, times] = run_tests(max_games_left, num_of_teams,
                                num_of_constraints, csv_type)

    # print('output')
    # print(output)
    # os.system('pwd')
    os.chdir('..')

    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)

        # write headers to csv file
        if os.stat(file_name).st_size == 0:
            writer.writerow(header)
        # print(times)
        writer.writerows(times)
