
# a GameState is a 2-ple of PlayerStates, where the first represents the current player, and the second, the opponent.
# a PlayerState is a 2-ple of Hands.
# a Hand is a number betwee 0 inclusive and 5 exclusive.

class Win:
    pass

class Lose:
    pass

class Draw:
    pass

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

def copy_player(player):
    return (player[0], player[1])

def copy_state(state):
    return (copy_player(state[0]), copy_player(state[1]))

def valid_hand(h):
    return 0 <= h < 5

def valid_player(player):
    return valid_hand(player[0]) and valid_hand(player[1])

def valid_state(state):
    return valid_player(state[0]) and valid_player(state[1])

def switch_players(state):
    return (state[1], state[0])

def best_outcome(o1, o2):
    if isinstance(o1, Win) or isinstance(o2, Win):
        return Win()
    if isinstance(o1, Draw) or isinstance(o2, Draw):
        return Draw()

    return Lose()

# GameState, Set[GameState], Map[GameState, Result] -> Result
def solve(state, seen, known):
    if is_game_over(state):
        if first_player_winner(state):
            # whatever
            pass
        else:
            # also whatever
            pass
        return

    if state in known:
        return known[state]

    if state in seen:
        known[state] = Draw() # is this the right thing to do? also, TODO when copy, when not copy? every recursive call on new state?
        return Draw()

    best_res = Lose()

    seen.add(state)
    # subtract left from left

    # how to check for validity? and where?
    ll_move = ((inc_hand(state[1][0], state[0][0]), state[1][1]), copy_player(state[0]))
    best_res = best_outcome(best_res, solve(ll_move, seen, known))

    lr_move = ((state[1][0], inc_hand(state[1][1], state[0][0])), copy_player(state[0])) # I don't actually need copy player, do I?
    best_res = best_outcome(best_res, solve(lr_move, seen, known))

    rl_move = ((inc_hand(state[1][0], state[0][1]), state[1][1]), copy_player(state[0]))
    best_res = best_outcome(best_res, solve(rl_move, seen, known))

    rr_move = ((state[1][0], inc_hand(state[1][1], state[0][1])), copy_player(state[0]))
    best_res = best_outcome(best_res, solve(rr_move, seen, known))

    # TODO split moves

    known[state] = best_res
    return best_res

    # otherwise, try every combo
    # there are 6 possible moves:
    # 1. subtract left from left
    # 2. subtract left from right
    # 3. subtract right from left
    # 4. subtract right from right
    # 5. split when left is 2 
    # 6. split when left is 4
    # 7. split when right is 2
    # 8. split when right is 4


