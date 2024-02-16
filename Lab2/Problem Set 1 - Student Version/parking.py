from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # Retrieves the initial state of the parking system.
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        for point in state:
            # Iterate through each point in the given state.
            
            if point in self.slots:
                # Check if the point is present in the parking slots.
                
                if self.slots[point] != state.index(point):
                    # Check if the index of the point in the state matches
                    # the expected index stored in the parking slots.
                    
                    return False
            else:
                # If the point is not present in the parking slots, it's not a goal state.
                return False

        # If all points pass the conditions, the state is considered a goal state.
        return True
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # Initialize an empty list to store possible actions.
        possible_actions = []

        # Iterate through each point in the given state.
        for point in state:
            # Iterate through each possible direction (assuming 'Direction' is an Enum).
            for direction in Direction:
                # Calculate the new point based on the current point and direction.
                new_point = point + direction.to_vector()

                # Check if the new point is within the boundaries of the parking area,
                # is part of the passages, and is not already present in the current state.
                if (
                    0 <= new_point.x < self.width
                    and 0 <= new_point.y < self.height
                    and new_point in self.passages
                    and new_point not in state
                ):
                    # If all conditions are met, add the action as a (index, direction) tuple.
                    possible_actions.append((state.index(point), direction))

        # Return the list of possible actions.
        return possible_actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # Unpack the action tuple into index and direction.
        index, direction = action

        # Initialize a new list to represent the successor state.
        new_state = []

        # Get the current point at the specified index in the current state.
        current_point = state[index]

        # Calculate the new point based on the current point and direction.
        new_point = current_point + direction.to_vector()

        # Update the point in the state at the specified index with the new point.
        new_state.insert(index, new_point)

        # Iterate through the rest of the state and insert points accordingly.
        for i in range(len(state)):
            if i != index:
                new_state.insert(i, state[i])

        # Return the successor state after applying the action.
        return new_state
            
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        # Initialize the cost variable.
        cost = 0

        # Unpack the action tuple into index and direction.
        index, direction = action

        # Get the current point at the specified index in the current state.
        current_point = state[index]

        # Calculate the new point based on the current point and direction.
        new_point = current_point + direction.to_vector()

        # Check if the new point corresponds to a parking slot and is not the expected slot.
        if new_point in self.slots and self.slots[new_point] != index:
            # If true, add a high cost (e.g., 100) to discourage undesired movements.
            cost += 100

        # Add a cost based on the index to encourage reaching the goal quickly.
        cost += 26 - index

        # Return the calculated cost for the given action.
        return cost
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
# print(ParkingProblem.from_file('parks/park1.txt'))