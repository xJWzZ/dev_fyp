import os
from sys import argv

# 1 game left to 18 games left
max_games_left = int(argv[1])
max_num_of_constraints = int(argv[2])

if os.path.exists('LeagueTestMiniZinc'):
    os.system('rm -r LeagueTestMiniZinc')

os.mkdir('LeagueTestMiniZinc')
os.chdir('LeagueTestMiniZinc')

# os.mkdir('1GamesLeft')
# os.chdir('1GamesLeft')

# for i in range(10):
#     games_played = 380 - (1*10)
#     num_of_constraints = 2
#     os.system('python3 ../../create_params.py 1GamesLeftDataset%d.dzn %d %d'
#         % (i, games_played, num_of_constraints))
# os.chdir('../..')
# os.system('rm -r LeagueTestMiniZinc')

for i in range(1, max_games_left + 1):
    os.mkdir('%dGamesLeft' % i)
    os.chdir('%dGamesLeft' % i)
    for num_of_constraints in range(1, max_num_of_constraints + 1):
        os.mkdir('%dConstraints' % num_of_constraints)
        os.chdir('%dConstraints' % num_of_constraints)
        for j in range(10):
            games_played = 380 - (i*10)
            # num_of_constraints to be changed.
            # num_of_constraints = 2
            os.system('python3 ../../../create_params.py %dGamesLeft%dConstraintsDataset%d.dzn %d %d'
                % (i, num_of_constraints, j, games_played, num_of_constraints))
        os.chdir('..')
    os.chdir('..')
