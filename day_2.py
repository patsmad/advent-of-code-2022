from get_input import get_input

day_num = 2
raw_input = get_input(day_num)

letter_to_score = lambda x: (ord(x) - 64) % 23
opp_player_to_score = lambda opp, player: 3 * ((player - opp + 1) % 3) + player

def part_1_get_opp_player(line):
    return tuple(map(letter_to_score, line.split(' ')))

def part_2_get_opp_player(line):
    opp, player_diff = part_1_get_opp_player(line)
    return opp, (opp + player_diff) % 3 + 1

def get_score(opp_player_fnc, lines):
    return sum([opp_player_to_score(*opp_player_fnc(line)) for line in lines])

# part 1
print(get_score(part_1_get_opp_player, raw_input.split('\n')))

# part 2
print(get_score(part_2_get_opp_player, raw_input.split('\n')))

# Test
def run_test():
    index_to_word = ['Rock', 'Paper', 'Scissor']
    score_to_result = ['Lose', 'Draw', 'Win']
    for opp in ['A', 'B', 'C']:
        opp_word = index_to_word[letter_to_score(opp) - 1]
        for player in ['X', 'Y', 'Z']:
            player_word = index_to_word[letter_to_score(player) - 1]
            letter_score = letter_to_score(player)
            score = get_score(part_1_get_opp_player, [f'{opp} {player}'])
            result = score_to_result[(score - letter_to_score(player)) // 3]
            print(f'Player: {player_word}; Opponent: {opp_word}; '
                  f'{letter_score} + {score - letter_score} ({result}) = {score}')
