import time
import os
import signal
import subprocess, threading

average_times = []

os.chdir('LeagueTestMiniZinc')

os.chdir('1GamesLeft')
# for i in range(1,18+1):
    # os.chdir('%dGamesLeft' % i)
    # for j in range(10):
        # might have to use threading
        # None


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
        print(self.process.returncode)
        return self.process.returncode


times = []

for j in range(10):
    command = Command('minizinc --solver Gecode ../../dev_fyp.mzn 1GamesLeftDataset%d.dzn' % 0)
    # plotting how long each takes, or whether it terminates or not?
    start_time = time.time()
    command.run(timeout=15)
    end_time = time.time()

    times.append(end_time-start_time)

print(times)
