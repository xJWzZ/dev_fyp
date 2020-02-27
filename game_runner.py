import time
import os
import signal
import subprocess
import threading
from sys import argv
import csv
import concurrent.futures

average_times = []
thread_times = []


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            # print('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=True, preexec_fn=os.setsid)
            # self.process.communicate()
            # self.process.check_output(self.cmd, shell=True, preexec_fn=os.setsid)
            self.process.communicate()
            # thread_times.append(output.decode('utf-8')[0])
            return 0

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            # print('Terminating process')
            os.killpg(self.process.pid, signal.SIGTERM)
            thread.join()
        return self.process.returncode


times = []


def run_minizinc(selected_games_left, constraint_num, dataset_num):
    cmd = '''minizinc --output-time --solver Gecode ../../../dev_fyp.mzn %dGamesLeft%dConstraintsDataset%d.dzn''' % (selected_games_left, constraint_num, dataset_num)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode('utf-8')


# table.field_names = header


def run_tests(selected_games_left, num_of_teams, num_of_constraints):
    os.chdir('LeagueTestMiniZinc%dTeams' % num_of_teams)

    headers = []

    for game_left in range(1, selected_games_left+1):

        os.chdir('%dGamesLeft' % game_left)

        for constraint_num in range(1, num_of_constraints+1):
            os.chdir('%dConstraints' % (constraint_num))

            # Adding the headers
            if constraint_num == 1:
                headers = os.popen('mzn2feat -i ../../../dev_fyp.mzn -d %dGamesLeft%dConstraintsDataset0.dzn -p'
                                   % (game_left, constraint_num)).read()
                headers = headers.split(',')
                headers += ['number_of_teams', 'fixtures_left',
                            'number_of_constraints', 'runtime', 'fpoints']

            for dataset_num in range(10):
                output = os.popen('minizinc --output-time --time-limit 15000 --solver Gecode ../../../dev_fyp.mzn %dGamesLeft%dConstraintsDataset%d.dzn'
                                  % (game_left, constraint_num,
                                     dataset_num)).read()

                feature_values = os.popen('mzn2feat -i ../../../dev_fyp.mzn -d %dGamesLeft%dConstraintsDataset%d.dzn'
                                          % (game_left, constraint_num,
                                             dataset_num)).read()

                feature_values = feature_values.split(',')

                output = output.split('\n')

                fpoints = output[0]

                if fpoints == '=====UNKNOWN=====':
                    fpoints = '-1'

                # os.system('ls')
                # print(output)
                time_elapsed = output[1].split(' ')
                time_elapsed = time_elapsed[3]

                row = feature_values
                row += [num_of_teams, game_left, constraint_num,
                        time_elapsed, fpoints]
                # print('length of feature_values: %d, length of row: %d'
                #       % (len(feature_values), len(row)))
                times.append(row)
                print('%s teams, and %s constraints %s games left number %s'
                      % (num_of_teams, constraint_num, game_left, dataset_num))

            os.chdir('..')

        os.chdir('..')
    # print(headers)
    # print(times)
    return [headers, times]
