from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
import queue
#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # Check if the initial state is already a goal state.
    if problem.is_goal(initial_state):
        return []  # The initial state is the goal state

    # Initialize the frontier with a deque and a set for efficient state checks.
    frontier = deque()
    frontier_set = set()  # Use a set to efficiently check if a state is in the frontier

    # Add the initial state and an empty path to the frontier.
    frontier.append((initial_state, []))
    frontier_set.add(initial_state)

    # Initialize a set to keep track of explored states.
    explored = set()

    # Continue the search until the frontier is empty.
    while frontier:
        # Dequeue the current state and path from the frontier.
        current_state, path = frontier.popleft()
        # Remove the state from the set when dequeued to maintain frontier_set integrity.
        frontier_set.remove(current_state)
        # Add the current state to the set of explored states.
        explored.add(current_state)

        # Generate successor states for the current state using available actions.
        for action in problem.get_actions(current_state):
            next_state = problem.get_successor(current_state, action)

            # Check if the next state is not in explored or in the frontier set.
            if next_state not in explored and next_state not in frontier_set:
                # Create a new path by appending the current action to the existing path.
                new_path = path + [action]

                # Check if the next state is a goal state.
                if problem.is_goal(next_state):
                    return new_path  # Return the solution path.
                else:
                    # Add the next state and its path to the frontier and set.
                    frontier.append((next_state, new_path))
                    frontier_set.add(next_state)  # Add the next state to the set.

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # Initialize the frontier with the initial state and an empty path.
    frontier = [(initial_state, [])]  # Stack to store (state, path) pairs

    # Initialize a set to keep track of explored states.
    explored = set()

    # Continue the search until the frontier is empty.
    while frontier:
        # Pop the last state and path from the frontier (depth-first behavior).
        current_state, path = frontier.pop()

        # Check if the current state is a goal state.
        if problem.is_goal(current_state):
            return path  # Return the solution path.

        # Skip to the next iteration if the current state has already been explored.
        if current_state in explored:
            continue

        # Mark the current state as explored.
        explored.add(current_state)

        # Generate successor states for the current state using available actions.
        for action in problem.get_actions(current_state):
            next_state = problem.get_successor(current_state, action)

            # Create a new path by appending the current action to the existing path.
            new_path = path + [action]

            # Add the next state and its path to the frontier for further exploration.
            frontier.append((next_state, new_path))

    # Return None if the search concludes without finding a solution.
    return None

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
     # Use a Priority Queue to prioritize nodes based on cost.
    frontier = queue.PriorityQueue()

    # Initialize a set to keep track of explored states.
    explored = set()

    # Initialize the tie-breaker for nodes with equal cost.
    current_tie_breaker = 0

    # Create the initial node with cost, tie-breaker, state, and an empty path.
    initial_node = (0, current_tie_breaker, initial_state, [])
    frontier.put(initial_node)

    # Continue the search until the frontier is empty.
    while frontier.queue:
        # Check if the frontier is empty, indicating that no solution exists.
        if not frontier:
            return None

        # Retrieve the node with the lowest cost from the frontier.
        current_cost, _, current_state, path = frontier.get()

        # Check if the current state is a goal state.
        if problem.is_goal(current_state):
            return path  # Return the solution path.

        # Skip to the next iteration if the current state has already been explored.
        if current_state in explored:
            continue

        # Mark the current state as explored.
        explored.add(current_state)

        # Generate successor states for the current state using available actions.
        for action in problem.get_actions(current_state):
            next_state = problem.get_successor(current_state, action)
            new_cost = current_cost + problem.get_cost(current_state, action)
            new_path = path + [action]
            current_tie_breaker += 1  # Increment the tie-breaker

            # Check if the next state is not in explored or in the frontier.
            if next_state not in explored:
                if next_state not in frontier.queue:    
                    # If not in frontier, add the node to the priority queue.
                    frontier.put((new_cost, current_tie_breaker, next_state, new_path))
                else:
                    # If in frontier, update the node with lower cost.
                    for i, node in enumerate(frontier.queue):
                        if node[2] == next_state:
                            if new_cost < node[0]:
                                # Replace the old node with the new node in the frontier.
                                del frontier.queue[i]
                                frontier.put((new_cost, current_tie_breaker, next_state, new_path))
                                break

    # If no solution is found, return None.
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # Create a priority queue (frontier) to store nodes, prioritized by the sum of cost and heuristic estimate.
    frontier = queue.PriorityQueue()

    # Set to keep track of explored states.
    explored = set()

    # Counter for tie-breaking when nodes have equal priority.
    current_tie_breaker = 0

    # Create the initial node using the sum of cost and heuristic estimate of the initial state.
    initial_node = (0 + heuristic(problem, initial_state), current_tie_breaker, initial_state, [], 0, heuristic(problem, initial_state))

    # Enqueue the initial node into the frontier.
    frontier.put(initial_node)

    # While the frontier is not empty:
    while frontier.queue:
        # If the frontier is empty, return None as no solution is found.
        if not frontier:
            return None

        # Dequeue a node from the frontier with the lowest priority.
        _, _, current_state, path, cost, _ = frontier.get()

        # If the current state is a goal state, return the solution path.
        if problem.is_goal(current_state):
            return path

        # If the current state has already been explored, skip to the next iteration.
        if current_state in explored:
            continue

        # Add the current state to the explored set.
        explored.add(current_state)

        # Explore the neighbors of the current state:
        for action in problem.get_actions(current_state):
            next_state = problem.get_successor(current_state, action)
            new_cost = cost + problem.get_cost(current_state, action)
            new_heuristic = heuristic(problem, next_state)
            new_path = path + [action]
            current_tie_breaker += 1

            # If a neighbor is not in the explored set or the frontier, enqueue it with its priority.
            if next_state not in explored:
                if next_state not in frontier.queue:   
                    frontier.put((new_cost + new_heuristic, current_tie_breaker, next_state, new_path, new_cost, new_heuristic))
                # If a neighbor is in the frontier but has a lower priority, update the frontier with the new priority.
                else:
                    for i, (priority, _, state, _, _, _) in enumerate(frontier.queue):
                        if state == next_state:
                            if new_cost + new_heuristic < priority:
                                del frontier.queue[i]
                                frontier.put((new_cost + new_heuristic, current_tie_breaker, next_state, new_path, new_cost, new_heuristic))
                                break

    # If no solution is found, return None.
    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # Create a priority queue (frontier) to store nodes, prioritized by heuristic estimate.
    frontier = queue.PriorityQueue()

    # Set to keep track of explored states.
    explored = set()

    # Counter for tie-breaking when nodes have equal heuristic estimates.
    current_tie_breaker = 0

    # Create the initial node using the heuristic estimate of the initial state.
    initial_node = (heuristic(problem, initial_state), current_tie_breaker, initial_state, [])

    # Enqueue the initial node into the frontier.
    frontier.put(initial_node)

    # While the frontier is not empty:
    while frontier.queue:
        # If the frontier is empty, return None as no solution is found.
        if not frontier:
            return None

        # Dequeue a node from the frontier with the lowest heuristic estimate.
        _, _, current_state, path = frontier.get()

        # If the current state is a goal state, return the solution path.
        if problem.is_goal(current_state):
            return path

        # If the current state has already been explored, skip to the next iteration.
        if current_state in explored:
            continue

        # Add the current state to the explored set.
        explored.add(current_state)

        # Explore the neighbors of the current state:
        for action in problem.get_actions(current_state):
            next_state = problem.get_successor(current_state, action)
            new_heuristic = heuristic(problem, next_state)
            new_path = path + [action]
            current_tie_breaker += 1

            # If a neighbor is not in the explored set or the frontier, enqueue it with its path and heuristic estimate.
            if next_state not in explored:
                if next_state not in frontier.queue:  
                    frontier.put((new_heuristic, current_tie_breaker, next_state, new_path))
                # If a neighbor is in the frontier but has a lower heuristic estimate, update the frontier with the new estimate.
                else:
                    for i, (heuristic__, _, state, _, _, _) in enumerate(frontier.queue):
                        if state == next_state:
                            if new_heuristic < heuristic__:
                                del frontier.queue[i]
                                frontier.put((new_heuristic, current_tie_breaker, next_state, new_path))
                                break

    # If no solution is found, return None.
    return None