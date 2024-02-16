from sokoban import SokobanProblem, SokobanState
from mathutils import manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use

def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
      # Ensure that the heuristic_cache is initialized in the problem's cache.
    if "heuristic_cache" not in problem.cache():
        problem.cache()["heuristic_cache"] = {}

    # Retrieve the cache for heuristic values.
    cache = problem.cache()["heuristic_cache"]

    # Convert the state to a hashable key for caching.
    state_key = (state.player, frozenset(state.crates))

    # Check if the heuristic value is already in the cache.
    if state_key in cache:
        return cache[state_key]

    # Initialize the total heuristic value.
    total_heuristic = 0

    # Calculate the heuristic value for each crate position.
    for crate_position in state.crates:
        min_distance = float('inf')

        # Find the minimum distance to a goal position for each crate.
        for goal_position in problem.layout.goals:
            distance = abs(crate_position.x - goal_position.x) + abs(crate_position.y - goal_position.y)
            min_distance = min(min_distance, distance)

        total_heuristic += min_distance

    # Store the calculated heuristic value in the cache.
    cache[state_key] = total_heuristic

    # Return the total heuristic value for the state.
    return total_heuristic