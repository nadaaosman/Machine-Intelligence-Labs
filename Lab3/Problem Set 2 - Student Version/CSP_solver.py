from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
import copy
from operator import itemgetter
from typing import List, Tuple
# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # NotImplemented()
    # Iterate through each binary constraint involving the assigned variable
    for constraint in problem.constraints:
        # Check if the constraint is a binary constraint and involves the assigned variable
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:
            # Identify the other variable in the binary constraint
            other_variable = constraint.get_other(assigned_variable)
            # Skip the constraint if the other variable is already assigned
            if other_variable not in domains:
                continue
            # Filter the domain of the other variable based on the binary constraint
            new_domain = set()
            for value in domains[other_variable]:
                # Check if the binary constraint is satisfied with the assigned and other variable values
                if constraint.is_satisfied({assigned_variable: assigned_value, other_variable: value}):
                    new_domain.add(value)
            # Update the domain of the other variable
            domains[other_variable] = new_domain
            # Check if the updated domain becomes empty
            if not domains[other_variable]:
                # If the domain becomes empty, return False as the problem is not solvable
                return False
    # If no variable's domain becomes empty, return True indicating successful forward checking
    return True

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    # NotImplemented()
    # Create a copy of the domains to avoid modifying the original
    domains_copy = domains.copy()
    # Get the domain of the variable to assign
    values = domains_copy.get(variable_to_assign, set())
    # List to store tuples of (value, number of removed values)
    values_with_removals = []
    for value in values:
        num_removed_values = count_removed_values(problem, variable_to_assign, value, domains_copy)
        values_with_removals.append((value, num_removed_values))
    # Sort the list of values with removals using itemgetter for multiple keys
    result_values = sorted(values_with_removals, key=itemgetter(1, 0))
    # Extract the values from the sorted list
    return [value[0] for value in result_values]

def count_removed_values(problem: Problem, variable_to_assign: str, value: Any, domains_copy: Dict[str, set]) -> int:
     # Initialize the counter for the number of removed values
    num_removed_values = 0
    # Iterate over each constraint in the problem
    for constraint in problem.constraints:
        # Check if the constraint is binary and involves the variable to assign
        if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:
            # Get the other variable in the constraint besides the variable to assign
            other_variable = constraint.get_other(variable_to_assign)
            # Check if the other variable has a domain
            if other_variable in domains_copy:
                # Increment the counter for each value in the domain of the other variable
                num_removed_values += sum(
                    # Check if the assignment is not consistent with the constraint
                    not constraint.is_satisfied({variable_to_assign: value, other_variable: other_value})
                    for other_value in domains_copy[other_variable]
                )
    # Return the total number of removed values
    return num_removed_values

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    #  NotImplemented()
    # Apply one-Consistency to handle unary constraints
    if not one_consistency(problem):
        return None
    # Initialize the assignment
    assignment = {}
    # Start backtracking search with forward checking
    result =  backtracking(assignment, problem, problem.domains)
    return result

def backtracking(assignment: Assignment, problem: Problem, domains: Dict[str, set]) -> Optional[Assignment]:
    # Check if the assignment is complete
    if problem.is_complete(assignment):
        return assignment
    # Select the next unassigned variable using the MRV heuristic
    variable_to_assign = minimum_remaining_values(problem, domains)
    # Order the values for the selected variable using the least restraining value heuristic
    values_ordered = least_restraining_values(problem, variable_to_assign, domains)
    for value in values_ordered:
        # Create a copy of the current assignment to avoid modifying it
        assignment[variable_to_assign] = value
        # Apply forward checking to prune domains
        domains_copy = copy.deepcopy(domains)
        # Remove the assigned variable from the copy to represent the updated domains
        domains_copy.pop(variable_to_assign) 
        if forward_checking(problem, variable_to_assign, value, domains_copy):
            # Recursively explore the next assignment
            result = backtracking(assignment, problem, domains_copy)        
            # If a solution is found, return it
            if result is not None:
                return result
    # No solution found
    return None

# another solution but 5/8
# def solve(problem: Problem) -> Optional[Assignment]:
    # # Apply 1-Consistency to prune domains based on unary constraints
    # if not one_consistency(problem):
    #     return None
    # # Initialize stack for backtracking
    # stack = [({}, copy.deepcopy(problem.domains))]
    # while stack:
    #     current_assignment, current_domains = stack.pop()
    #     # Check if the assignment is complete
    #     if problem.is_complete(current_assignment):
    #         return current_assignment
    #     # Select the next unassigned variable using the MRV heuristic
    #     variable_to_assign = minimum_remaining_values(problem, current_domains)
    #     # Order the values for the selected variable using the least restraining value heuristic
    #     values_ordered = least_restraining_values(problem, variable_to_assign, current_domains)
    #     for value in values_ordered:
    #         # Create a copy of the current assignment to avoid modifying it
    #         new_assignment = current_assignment.copy()
    #         new_assignment[variable_to_assign] = value
    #         # Apply forward checking to prune domains
    #         new_domains = copy.deepcopy(current_domains)
    #         new_domains.pop(variable_to_assign,None)
    #         if forward_checking(problem, variable_to_assign, value, new_domains):
    #             # Push the new assignment and domains onto the stack
    #             stack.append((new_assignment, new_domains))
    # # No solution found
    # return None
    

