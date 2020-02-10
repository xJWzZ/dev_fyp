import os
from sys import argv
from create_params import create_params


def create_test_files(num_of_teams, max_games_left, max_num_of_constraints):
    # 1 game left to 18 games left
    print('creating test files')
    max_games_left = int(max_games_left)
    max_num_of_constraints = int(max_num_of_constraints)
    num_of_teams = int(num_of_teams)

    if os.path.exists('LeagueTestMiniZinc%dTeams' % num_of_teams):
        # os.system('rm -r LeagueTestMiniZinc%dTeams' % num_of_teams)
        print('exiting test files')
        return

    os.mkdir('LeagueTestMiniZinc%dTeams' % num_of_teams)
    os.chdir('LeagueTestMiniZinc%dTeams' % num_of_teams)

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
                games_played = (num_of_teams*(num_of_teams-1)) - (i*(num_of_teams/2))
                # num_of_constraints to be changed.
                # num_of_constraints = 2
                # os.system('python3 ../../../create_params.py %dGamesLeft%dConstraintsDataset%d.dzn %d %d %d'
                #     % (i, num_of_constraints, j, games_played, num_of_constraints, num_of_teams))
                create_params('%dGamesLeft%dConstraintsDataset%d.dzn' %
                              (i, num_of_constraints, j), games_played,
                              num_of_constraints, num_of_teams)
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')
