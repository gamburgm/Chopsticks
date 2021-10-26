
# a GameState is a 2-ple of PlayerStates, where the first represents the current player, and the second, the opponent.
# a PlayerState is a 2-ple of Hands.
# a Hand is a number betwee 0 inclusive and 5 exclusive.

class Win:
    def __str__(self):
        return "Win"

class Lose:
    def __str__(self):
        return "Lose"

class Draw:
    def __str__(self):
        return "Draw"

def inc_hand(h, val):
    return (h + val) % 5

def empty_hand(h):
    return h == 0

def is_eliminated(player):
    return empty_hand(player[0]) and empty_hand(player[1])

def is_game_over(state):
    return is_eliminated(state[0]) or is_eliminated(state[1])

def first_player_winner(state):
    return is_eliminated(state[1])

def valid_hand(h):
    return 0 <= h < 5

def valid_player(player):
    return valid_hand(player[0]) and valid_hand(player[1])

def valid_state(state):
    return valid_player(state[0]) and valid_player(state[1])

def switch_players(state):
    return (state[1], state[0])

def can_split(player):
    def splittable(h1, h2):
        return h1 == 0 and (h2 == 2 or h2 == 4)

    return splittable(player[0], player[1]) or splittable(player[1], player[0])

def split_player(player):
    if player[0] == 2 or player[1] == 2:
        return (1, 1)
    else:
        return (2, 2)

def best_outcome(o1, o2):
    if isinstance(o1, Win) or isinstance(o2, Win):
        return Win()
    if isinstance(o1, Draw) or isinstance(o2, Draw):
        return Draw()

    return Lose()

# GameState, Set[GameState], Map[GameState, Result] -> Result
def solve(state, seen, known):
    if state in known:
        return known[state]

    if is_game_over(state):
        if first_player_winner(state):
            known[state] = Win()
            return Win()
        else:
            known[state] = Lose()
            return Lose()

    if state in seen:
        known[state] = Draw() # is this the right thing to do? also, TODO when copy, when not copy? every recursive call on new state?
        return Draw()

    best_res = Lose()

    seen.add(state)

    first_left_empty = empty_hand(state[0][0])
    first_right_empty = empty_hand(state[0][1])
    second_left_empty = empty_hand(state[1][0])
    second_right_empty = empty_hand(state[1][1])

    if not first_left_empty and not second_left_empty:
        ll_move = ((inc_hand(state[1][0], state[0][0]), state[1][1]), state[0])
        best_res = best_outcome(best_res, flip_result(solve(ll_move, seen, known)))

    if not first_left_empty and not second_right_empty:
        lr_move = ((state[1][0], inc_hand(state[1][1], state[0][0])), state[0]) # I don't actually need copy player, do I?
        best_res = best_outcome(best_res, flip_result(solve(lr_move, seen, known)))

    if not first_right_empty and not second_left_empty:
        rl_move = ((inc_hand(state[1][0], state[0][1]), state[1][1]), state[0])
        best_res = best_outcome(best_res, flip_result(solve(rl_move, seen, known)))

    if not first_right_empty and not second_right_empty:
        rr_move = ((state[1][0], inc_hand(state[1][1], state[0][1])), state[0])
        best_res = best_outcome(best_res, flip_result(solve(rr_move, seen, known)))

    if can_split(state[0]):
        new_p = split_player(state[0])
        new_state = (state[1], new_p)
        best_res = best_outcome(best_res, flip_result(solve(new_state, seen, known)))

    known[state] = best_res
    return best_res

print(solve(((1, 1), (1, 1)), set(), {}))
