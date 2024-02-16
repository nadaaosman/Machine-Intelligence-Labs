from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        if self.mdp.is_terminal(state):
        # Check if the given state is terminal
        # If the state is terminal, return 0 because there are no future rewards or transitions from terminal states
            return 0
        else:   
        # Compute the Bellman utility for the non-terminal state
        # The Bellman equation calculates the utility of a state by considering the maximum expected utility among all possible actions
        # It involves summing over the successor states for each action and choosing the maximum overall action
        # The formula: U(s) = max_a sum_s' P(s'|s,a) * (R(s,a,s') + gamma * U(s'))
        # Here, we use a nested list comprehension to iterate over actions and successor states
        # The outer list comprehension iterates over actions, and the inner one iterates over successor states for each action
        # We calculate the expected utility for each action and choose the maximum among them         
         max_utility = max(
    sum(
        self.mdp.get_successor(state, action)[next_state] *
        (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
        for next_state in self.mdp.get_successor(state, action)
    )
    for action in self.mdp.get_actions(state))
         return max_utility

          
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()
        # Calculate new utilities for all states using the Bellman equation and store in a dictionary
        updated_utilities = dict(map(lambda state: (state, self.compute_bellman(state)), self.mdp.get_states()))
        # Calculate the maximum change in utility among all states
        max_utility = max(map(lambda state: abs(updated_utilities[state] - self.utilities[state]), self.mdp.get_states()))
        # Check if the maximum change is within the specified tolerance
        if max_utility <= tolerance:
             # Update utilities and indicate that convergence has been reached
            self.utilities = updated_utilities
            return True
        else:
            # Update utilities and indicate that convergence has not been reached
            self.utilities = updated_utilities
            return False

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        # NotImplemented()
        # Initialize the iteration counter
        each_iteration = 0
          # Continue the loop until the specified number of iterations is reached or convergence
        while iterations is None or each_iteration < iterations:
            # Increment the iteration counter
            each_iteration =each_iteration+ 1
            # Check if the utilities have converged; break the loop if true
            if self.update(tolerance):
                break
            # Return the total number of iterations performed
        return each_iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        # Check if the current state is terminal
        if self.mdp.is_terminal(state):
        # If the state is terminal, return None as there is no action to take
            return None
        else:
        # Find the action with the maximum expected utility using the Bellman equation
        # The max function is used with a key function that calculates the sum of expected utilities for each action
          max_action = max(self.mdp.get_actions(state),
                           key=lambda action: sum(self.mdp.get_successor(state, action)[next_state] *(self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])
                            for next_state in self.mdp.get_successor(state, action)))
        # Return the action with the maximum expected utility
          return max_action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
