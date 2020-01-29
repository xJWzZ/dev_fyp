import time
import os
import signal
import subprocess
import threading
from sys import argv
from prettytable import PrettyTable
import csv

average_times = []

selected_games_left = int(argv[1])

os.chdir('LeagueTestMiniZinc')

os.chdir('%dGamesLeft' % selected_games_left)


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            # print('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=True, preexec_fn=os.setsid)
            self.process.communicate()
            # print('Thread finished')
            return 0

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            # print('Terminating process')
            os.killpg(self.process.pid, signal.SIGTERM)
            thread.join()
        return self.process.returncode

header = ['Num of Constraints for %d games left' % (selected_games_left), 'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'time7', 'time8', 'time9', 'time10']

times = []

table = PrettyTable()

table.field_names = header



for constraint_num in range(1, 4):
    constraint_times = [constraint_num]
    os.chdir('%dConstraints' % (constraint_num))
    for dataset_num in range(10):
        command = Command('''minizinc --solver Gecode ../../../dev_fyp.mzn %dGamesLeft%dConstraintsDataset%d.dzn'''
                          % (selected_games_left, constraint_num, dataset_num))
        # plotting how long each takes, or whether it terminates or not?
        start_time = time.time()
        command.run(timeout=15)
        end_time = time.time()

        constraint_times.append(round(end_time - start_time, 6))
    os.chdir('..')
    # print(constraint_times)
    times.append(constraint_times)
    table.add_row(constraint_times)
    # times.append(constraint_times)

    # times.append(round(end_time-start_time, 6))
print(table)
print(times)
# print(times)
