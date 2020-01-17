import copy
from random import randint, shuffle
from datetime import datetime
from sys import argv

handler = open(argv[1], "w+")

num_of_teams = 20
num_of_fixtures_played = argv[2]
num_of_constraints = argv[3]


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

# Generate the table
table = {}
for i in range(1, num_of_teams+1):
    table[i] = 0

# iterate through each game in the shuffled list.
# after each game, update the table accordingly
# print('num_of_fixtures_played')
# print(num_of_fixtures_played)
# print('allgames')
# print(all_games[300])
all_games_copy = copy.deepcopy(all_games)
# print(len(all_games))
for i in range(num_of_fixtures_played):
    # print(i)
    game_to_play = all_games_copy[i]
    (team1, team2) = game_to_play
    results[(team1, team2)] = 1
    result_of_game = randint(0, 2)
    all_games.remove(game_to_play)
    if result_of_game == 0:
        table[team1] += 3
    elif result_of_game == 2:
        table[team2] += 3
    else:
        table[team1] += 1
        table[team2] += 1
# print(len(all_games))
now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

# introduce a time limit for executing instances in minizinc command line
# total no of games = 30
# games left up to 18
# do each no of teams 10 times
# cactus plot: number of given instances we can plot in a given time


handler.write("""
%%FILE DATA:	Soccer Computational Problem for MiniZinc Models	%%
%%AUTHOR:	Jack Wall	%%
%%CONTACT:  	116397063@umail.ucc.ie			%%
%%LAST UPDATE:	%s						%%
%%DESCRIPTION: 	%d games played with %d games left				%%
""" % (now, num_of_fixtures_played, len(all_games)))

handler.write('\nn=%d; %%number of teams\n' % num_of_teams)

formatted_games_to_play = '['

for game in all_games:
    formatted_games_to_play += '|%d,%d' % (game[0], game[1])
formatted_games_to_play += '|];'

# print('games to play: ' + formatted_games_to_play)

handler.write('\n%%Games to play\ngames=%s\n' % formatted_games_to_play)

formatted_table = '['
for i in table:
    formatted_table += '%d,' % table[i]
formatted_table = formatted_table[:-1]
formatted_table += '];'
# print('current table: ' + formatted_table)

handler.write('\n%%Initial points\niPoints=%s\n' % formatted_table)

# need to create the constraints.
# random team number, random constraint, then random team number thats not the
# first team number.
# check to see if it runs.
# get it to make it in a file structure like the test set.
# make the running set
# make a bash script that runs this then runs the running set.

# creating constraints
constraints = []
formatted_constraints = "["
for _ in range(num_of_constraints):
    team1 = randint(1, num_of_teams)
    team2 = randint(1, num_of_teams)
    while team2 == team1:
        team2 = randint(1, num_of_teams)
    constraint = randint(1, 4)
    constraints += [[team1, constraint, team2]]

# print(constraints)

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
