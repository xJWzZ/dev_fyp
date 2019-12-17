import copy
from random import randint, shuffle
from datetime import datetime

handler = open('test_data.mzn', "w+")

# num_of_teams = input("Enter number of teams:\n")
# num_of_fixtures_played = input("Enter Number of fixtures played:\n")
num_of_teams = "4"
num_of_fixtures_played = "2"

num_of_teams = int(num_of_teams)

if num_of_teams % 2 == 1:
    print("Error: Number of teams must be an even number")
    exit()

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

# print(list(range(1, len(fixtures)+1)))
fixture_numbers = list(range(1, len(fixtures)+1))

# not gonna work when there's 3 games left for every team
print(all_games)
shuffle(all_games)

# Generate the table
table = {}
for i in range(1, num_of_teams+1):
    table[i] = 0

# iterate through each game in the shuffled list.
# after each game, update the table accordingly
for i in range(num_of_fixtures_played):
    game_to_play = all_games[i]
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

formatted_games_to_play = '['

for game in all_games:
    formatted_games_to_play += '|%d,%d' % (game[0], game[1])
formatted_games_to_play += '|];'

print('games to play: ' + formatted_games_to_play)

formatted_table = '['
for i in table:
    formatted_table += '%d,' % table[i]
formatted_table = formatted_table[:-1]
formatted_table += '];'
print('current table: ' + formatted_table)

# game assignment to appropriate fixture.
'''for team1 in range(1, num_of_teams):
    fixtures_to_be_assigned = copy.deepcopy(fixture_numbers)
    # going through all the fixtures and assigning team1's games
    # to every fixture in the form (team1, team2)
    for team2 in range(team1, num_of_teams+1):
        fixture_index = randint(0, len(fixtures_to_be_assigned))
        fixtures[fixture_index].append((team1, team2))
        if len(fixtures_to_be_assigned) == 0:
            fixtures_to_be_assigned = copy.deepcopy(fixture_numbers)
    # same thing but for the form (team2, team1)
    for team2 in range(team1, num_of_teams+1):
        fixture_index = randint(0, len(fixtures_to_be_assigned))
        # #################################################################################
        # problem here: fixtures[fixture_index] is the location of the tuple
        # we need the direct values of the tuple however
        while (team2 not in fixtures[fixture_index]) and \
            (team1 not in fixtures[fixture_index]):
            fixture_index = randint(0, len(fixtures_to_be_assigned))
        fixtures[fixture_index].append((team2, team1))
        if len(fixtures_to_be_assigned) == 0:
            fixtures_to_be_assigned = copy.deepcopy(fixture_numbers)'''
# fixtures_to_be_assigned = copy.deepcopy(results)
# for team1 in range(total_fixtures):


# for i in range(5):
#     handler.write("test\n")
