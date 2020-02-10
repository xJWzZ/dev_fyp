import copy
from random import randint, shuffle
from datetime import datetime
from sys import argv


def create_params(file, num_of_fixtures_played, num_of_constraints, num_of_teams):

    handler = open(file, "w+")

    num_of_teams = int(num_of_teams)

    num_of_constraints = int(num_of_constraints)

    num_of_fixtures_played = int(num_of_fixtures_played)

    teams = []
    total_fixtures = num_of_teams*(num_of_teams-1)

    for i in range(1, num_of_teams+1):
        teams.append(i)

    # fixtures is a dictionary with keys as the game (team1, team2)
    # and the result, -1 if not played.
    results = {}

    # fixtures contains which games are being played at which fixture
    fixtures = []

    # all_games contains the order in which the games are
    # played in.
    all_games = []

    # first, generate all the possible games
    for i in range(1, len(teams)+1):
        for j in range(i, len(teams)+1):
            if i != j:
                results[(i, j)] = -1
                all_games.append((i, j))

    # Everyone plays twice so must reverse the keys
    # and add them too.
    temp_reverse_results = []
    for key in results:
        temp_reverse_results.append((key[1], key[0]))

    for fixture in temp_reverse_results:
        results[fixture] = -1
        all_games.append(fixture)

    # for each team, they must play every other team twice
    # this assigns each game to a fixture
    results_to_be_assigned = copy.deepcopy(results)
    for fixture in range((num_of_teams-1)*2):
        # add a new fixture
        fixtures.append([])

    fixture_numbers = list(range(1, len(fixtures)+1))

    # not gonna work when there's 3 games left for every team
    # print(len(all_games))
    shuffle(all_games)

    # Generate the completed_table
    completed_table = {}
    uncompleted_table = {}
    for i in range(1, num_of_teams+1):
        completed_table[i] = 0

    # iterate through each game in the shuffled list.
    # after each game, update the completed_table accordingly
    # print('num_of_fixtures_played')
    # print(num_of_fixtures_played)
    # print('allgames')
    # print(all_games[300])
    all_games_copy = copy.deepcopy(all_games)

    # simulate all games.
    for i in range(num_of_teams*(num_of_teams-1)):
        # print(i)
        if i == num_of_fixtures_played+1:
            uncompleted_table = copy.deepcopy(completed_table)
        game_to_play = all_games_copy[i]
        (team1, team2) = game_to_play
        results[(team1, team2)] = 1
        result_of_game = randint(0, 2)
        if i < num_of_fixtures_played:
            all_games.remove(game_to_play)
        if result_of_game == 0:
            completed_table[team1] += 3
        elif result_of_game == 2:
            completed_table[team2] += 3
        else:
            completed_table[team1] += 1
            completed_table[team2] += 1
    # print(len(all_games))
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    constraints = []
    formatted_constraints = "["

    end_table = []

    for i in completed_table:
        end_table.append((completed_table[i], i))

    end_table.sort()
    end_table.reverse()
    # print(end_table)

    # Assigning constraints
    for i in range(num_of_constraints):
        eq = randint(1, 5)
        # Edge cases
        if (eq == 2) & (i == 0):
            eq += 1
        if (eq == 4) & (i == num_of_constraints-1):
            eq += 1

        # Normal cases
        if eq == 1:
            constraints += [[end_table[i][1], 1, i+1]]
        elif eq == 2:
            constraints += [[end_table[i][1], 2, i]]
        elif eq == 3:
            constraints += [[end_table[i][1], 3, i+1]]
        elif eq == 4:
            constraints += [[end_table[i][1], 4, i+2]]
        elif eq == 5:
            constraints += [[end_table[i][1], 5, i+1]]

    handler.write("""
%%FILE DATA:	Soccer Computational Problem for MiniZinc Models	%%
%%AUTHOR:	Jack Wall	%%
%%CONTACT:  	116397063@umail.ucc.ie			%%
%%LAST UPDATE:	%s						%%
%%DESCRIPTION: 	%d games played with %d games left				%%\n
""" % (now, num_of_fixtures_played, len(all_games)))

    handler.write('\nn=%d; %%number of teams\n' % num_of_teams)

    formatted_games_to_play = '['

    for game in all_games:
        formatted_games_to_play += '|%d,%d' % (game[0], game[1])
    formatted_games_to_play += '|];'

    handler.write('\n%%Games to play\ngames=%s\n' % formatted_games_to_play)

    formatted_uncompleted_table = '['
    for i in uncompleted_table:
        formatted_uncompleted_table += '%d,' % uncompleted_table[i]
    formatted_uncompleted_table = formatted_uncompleted_table[:-1]
    formatted_uncompleted_table += '];'

    handler.write('\n%%Initial points\niPoints=%s\n' % formatted_uncompleted_table)

    # format constraints
    for constraint in constraints:
        formatted_constraints += '|%d,%d,%d' % \
            (constraint[0], constraint[1], constraint[2])
    formatted_constraints += '|];'

    handler.write('''
%POSITION CONSTRAINTS
% [|teamID, operator, position|...]
% operators index:
%  1 for =  operator
%  2 for >  operator
%  3 for >= operator
%  4 for <  operator
%  5 for <= operator
''')

    handler.write('positionConstraints=%s' % formatted_constraints)
