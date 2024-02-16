from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import math
#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    # Get the current player's turn using the game state
    player_turn = game.get_turn(state)
    # Check if the current state is a terminal state and get the values for all players
    is_terminal, values = game.is_terminal(state)
    # If the state is terminal, return the values for the current player and None as there is no action
    if is_terminal:
        return values[player_turn], None
    # If the maximum depth is reached, return the heuristic value and None for action
    if max_depth == 0:
        return (heuristic(game, state, player_turn), None) if player_turn == 0 else (-heuristic(game, state, player_turn), None)
    # Generate a list of tuples containing possible actions and their resulting states
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    # If it's the player's turn, perform a max operation to choose the action with the maximum heuristic value
    if player_turn == 0:
        value, _, action = max((minimax(game, state, heuristic, max_depth - 1)[0], -index, action) for index, (action, state) in enumerate(actions_states))
    # If it's the opponent's turn, perform a min operation to choose the action with the minimum heuristic value
    else:
        value, _, action = min((minimax(game, state, heuristic, max_depth - 1)[0], -index, action) for index, (action, state) in enumerate(actions_states))
    # Return the final value and the chosen action
    return value, action

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax

def alphabeta_recursive(current_state: S, alpha, beta,heuristic: HeuristicFunction,game: Game[S, A],current_depth: int = -1) -> Tuple[float, A]:
    # Get the current player's turn and check if the current state is terminal
    current_player = game.get_turn(current_state)
    is_terminal, state_values = game.is_terminal(current_state)
    # If the state is terminal, return the values
    if is_terminal:
        return state_values[current_player], None
    # If the depth is 0, return the heuristic value for the current player
    if current_depth == 0:
        if current_player == 0:
            return heuristic(game, current_state, current_player), None
        else:
            # For the opponent, return the negative of the heuristic value
            return -heuristic(game, current_state, current_player), None
    # If it's the player's turn (max node), find the action leading to the maximum value
    if current_player == 0:
        best_eval = float('-inf')
        best_action = None
        for current_action in game.get_actions(current_state):
            # evaluate the successor state
            result, _ = alphabeta_recursive(game.get_successor(current_state, current_action), alpha, beta, heuristic, game, current_depth - 1)   
            # Update the best evaluation and action
            if result > best_eval:
                best_eval = result
                best_action = current_action   
            # Update alpha, as it represents the best (maximum) evaluation so far
            alpha = max(alpha, result)   
            # Prune the remaining branch if beta is less than or equal to alpha
            if beta <= alpha:
                break
        # Return the best evaluation and corresponding action
        return best_eval, best_action
    # If it's the opponent's turn (min node), find the action leading to the minimum value
    else:
        lowest_eval = float('inf')
        best_action = None
        for current_action in game.get_actions(current_state):
            # evaluate the successor state
            eval_result, _ = alphabeta_recursive(game.get_successor(current_state, current_action), alpha, beta, heuristic, game, current_depth - 1)          
            # Update the best (lowest) evaluation and corresponding action
            if eval_result < lowest_eval:
                lowest_eval = eval_result
                best_action = current_action        
            # Update beta, as it represents the best (minimum) evaluation so far
            beta = min(beta, eval_result)        
            # Prune the remaining branch if beta is less than or equal to alpha
            if beta <= alpha:
                break      
        # Return the lowest evaluation and corresponding action
        return lowest_eval, best_action
        
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    return alphabeta_recursive(state, float('-inf'), float('inf'), heuristic,game,max_depth)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_recursive_with_move_ordering(game: Game[S, A],current_state: S, alpha, beta,heuristic: HeuristicFunction, depth: int = -1)-> Tuple[float, A]:
     # Get the current player in the game
    current_player = game.get_turn(current_state)
    # Check if the current state is terminal
    is_terminal, terminal_values = game.is_terminal(current_state)
    # If terminal, return the terminal values for the current player
    if is_terminal:
        if current_player == 0:
            return terminal_values[current_player], None
        else:
            return -terminal_values[current_player], None
    # If the maximum depth is reached, return the heuristic value for the current player
    if depth == 0:
        if current_player == 0:
            return heuristic(game, current_state, current_player), None
        else:
            return -heuristic(game, current_state, current_player), None
    # Generate a list of actions and their resulting states
    actions_and_states = [(action, game.get_successor(current_state, action)) for action in game.get_actions(current_state)]
    # If it's the player's turn (max node), sort actions based on heuristic values in descending order
    if current_player == 0:
        sorted_actions_and_states = sorted(actions_and_states, key=lambda x: heuristic(game, x[1], current_player), reverse=current_player == 0)
        maximum_eval = -math.inf
        maximum_action = None
        # Iterate through sorted actions and states
        for action, successor_state in sorted_actions_and_states:
            # evaluate the successor state
            evaluation, _ = alphabeta_recursive_with_move_ordering(game, successor_state, alpha, beta, heuristic, depth - 1)
            # Update maximum evaluation and corresponding action
            if evaluation > maximum_eval:
                maximum_eval = evaluation
                maximum_action = action
            # Update alpha with the maximum evaluation
            alpha = max(alpha, evaluation)
            # If beta is less than or equal to alpha, prune the search
            if beta <= alpha:
                break
        return maximum_eval, maximum_action
    else:
        # If it's the opponent's turn (min node), sort actions based on heuristic values in ascending order
        sorted_actions_and_states = sorted(actions_and_states, key=lambda x: -heuristic(game, x[1], current_player), reverse=current_player == 0)
        minimum_eval = math.inf
        minimum_action = None
        # Iterate through sorted actions and states
        for action, successor_state in sorted_actions_and_states:
            # evaluate the successor state
            evaluation, _ = alphabeta_recursive_with_move_ordering(game, successor_state, alpha, beta, heuristic, depth - 1)
            # Update minimum evaluation and corresponding action
            if evaluation < minimum_eval:
                minimum_eval = evaluation
                minimum_action = action
            # Update beta with the minimum evaluation
            beta = min(beta, evaluation)
            # If beta is less than or equal to alpha, prune the search
            if beta <= alpha:
                break
        return minimum_eval, minimum_action
    
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    return alphabeta_recursive_with_move_ordering(game,state, -math.inf, math.inf, heuristic,max_depth)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    # Check if the current state is terminal
    is_terminal, values = game.is_terminal(state)
    # If terminal, return the terminal values
    if is_terminal:
        return values[0], None
    # If the maximum depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, 0), None
    # Get the current player
    current_player = game.get_turn(state)
    # If it's the player's turn (max node), find the action with the maximum heuristic value
    if current_player == 0:
        max_eval = -float('inf')
        max_action = None
        # Iterate through all possible actions
        for action in game.get_actions(state):
            # Get the successor state after applying the action
            successor_state = game.get_successor(state, action)
            # expectimax for the successor state
            eval, _ = expectimax(game, successor_state, heuristic, max_depth - 1)
            # Update max_eval and corresponding action
            if eval > max_eval:
                max_eval = eval
                max_action = action
        return max_eval, max_action
    else:
        # If it's the monster's turn (chance node), calculate the average evaluation for all possible outcomes
        average_eval = 0.0
        num_actions = len(game.get_actions(state))
        # Iterate through all possible actions
        for action in game.get_actions(state):
            # Get the successor state after applying the action
            successor_state = game.get_successor(state, action)
            # expectimax for the successor state
            eval, _ = expectimax(game, successor_state, heuristic, max_depth - 1)
            # Accumulate the evaluations
            average_eval += eval / num_actions
        return average_eval, None