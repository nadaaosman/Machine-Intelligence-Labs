from typing import Tuple,Set
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS
        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        problem.variables = []
        problem.domains = {}
        problem.constraints = []
            # Define variables
        letters = set(LHS0 + LHS1 + RHS)
        problem.variables = list(letters)
        # Define domains
        problem.domains = {letter: set(range(10)) for letter in letters}
        # Define constraints
        # Unary constraints for the first letter of each term to be non-zero
        for term in [LHS0, LHS1, RHS]:
            problem.constraints.append(UnaryConstraint(term[0], lambda x: x != 0))
        # Binary constraints for different letters to have different values
        for letter1 in letters:
            for letter2 in letters:
                if letter1 != letter2:
                    problem.constraints.append(
                        BinaryConstraint((letter1, letter2), lambda x, y: x != y)
                    )
          # Create auxiliary variables for each pair of letters
        for i in range(min(len(LHS0),len(LHS1))):
                    letter1=LHS0[i]
                    letter2=LHS1[i]
                    mixed=LHS0[i]+LHS1[i]
                    aux_var_name = f"{mixed}"
                    alo= f"{LHS0[i]}+{LHS1[i]}"
                    problem.variables.append(aux_var_name)
                    problem.domains[aux_var_name] = set(range(10))
                    print("alo",alo)
                    print("aux",aux_var_name)
                    # Constraint: Unary constraint on the auxiliary variable to be the sum of the two letters
                    problem.constraints.append(
                        BinaryConstraint((letter1,letter2,mixed),lambda x,y,z:z== (x + y) == z))
                    
        # Additional constraints
        if len(RHS) >= max(len(LHS0), len(LHS1)) and len(LHS0)==len(LHS1):
            last_letter_RHS = RHS[0]
            problem.constraints.append(UnaryConstraint(last_letter_RHS, lambda x: x == 1))
            for letter in letters:
                if letter !=last_letter_RHS:
                    problem.constraints.append(UnaryConstraint(letter, lambda x: x != 1))
            #   # Constraint: Sum of two variables before the last one from the left must be greater than 9
            # second_last_letter_RHS = LHS0[0] 
            # third_last_letter_RHS = LHS1[0] 
            # problem.constraints.append(
            #     BinaryConstraint(
            #         (third_last_letter_RHS, second_last_letter_RHS),
            #         lambda x, y: x + y > 9
            #     )
            # )
        max_len = max(len(LHS0), len(LHS1), len(RHS))
        for i in range(max_len - 1, -1, -1):
            z = RHS[i]  
            if i < len(LHS0) and i < len(LHS1):
                   x = LHS0[i]
                   y = LHS1[i]
                   xy=x+y
                   problem.constraints.append(BinaryConstraint((xy, z),lambda xy, z: xy == z))
            elif i < len(LHS0):
                    x = LHS0[i]
                    problem.constraints.append(BinaryConstraint((x, z),lambda x, z: x == z))
            elif i < len(LHS1):
                y = LHS1[i]
                problem.constraints.append(BinaryConstraint((y, z),lambda y, z: y == z))   
        return problem
    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
        










    #         @staticmethod
    # def from_text(text: str) -> 'CryptArithmeticProblem':
    #     # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
    #     # matches and extracts LHS0, LHS1 & RHS
    #     # For example, it would parse "SEND + MORE = MONEY" and extract the
    #     # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
    #     pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
    #     match = re.match(pattern, text)
    #     if not match: raise Exception("Failed to parse:" + text)
    #     LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

    #     problem = CryptArithmeticProblem()
    #     problem.LHS = (LHS0, LHS1)
    #     problem.RHS = RHS
    #     #TODO Edit and complete the rest of this function
    #     # problem.variables:    should contain a list of variables where each variable is string (the variable name)
    #     # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
    #     #                       For the letters, the domain can only contain integers in the range [0,9].
    #     # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
    #     problem.variables = []
    #     problem.domains = {}
    #     problem.constraints = []
    #         # Define variables
    #     letters = set(LHS0 + LHS1 + RHS)
    #     problem.variables = list(letters)
    #     # Define domains
    #     problem.domains = {letter: set(range(10)) for letter in letters}
    #     # Define constraints
    #     # Unary constraints for the first letter of each term to be non-zero
    #     for term in [LHS0, LHS1, RHS]:
    #         problem.constraints.append(UnaryConstraint(term[0], lambda x: x != 0))
    #     # Binary constraints for different letters to have different values
    #     for letter1 in letters:
    #         for letter2 in letters:
    #             if letter1 != letter2:
    #                 problem.constraints.append(
    #                     BinaryConstraint((letter1, letter2), lambda x, y: x != y)
    #                 )
    #       # Create auxiliary variables for each pair of letters
    #     aux_variables = {}
    #     for i in range(min(len(LHS0),len(LHS1))):
    #                 letter_LHS0 = LHS0[i]
    #                 letter_LHS1 = LHS1[i]
    #                 aux_var_name = f"{letter_LHS0}{letter_LHS1}"
    #                 # print("aux_var_name",aux_var_name)
    #                 aux_variables[(letter_LHS0, letter_LHS1)] = aux_var_name
    #                 problem.variables.append(aux_var_name)
    #                 problem.domains[aux_var_name] = set(range(19))
    #                 # Constraint: Unary constraint on the auxiliary variable to be the sum of the two letters
    #                 problem.constraints.append(
    #                     UnaryConstraint(aux_var_name,lambda x:x==letter_LHS0+ letter_LHS1)
    #                 )
    #     # Additional constraints
    #     if len(RHS) >= max(len(LHS0), len(LHS1)) and len(LHS0)==len(LHS1):
    #         last_letter_RHS = RHS[0]
    #         problem.constraints.append(UnaryConstraint(last_letter_RHS, lambda x: x == 1))
    #         for letter in letters:
    #             if letter !=last_letter_RHS:
    #                 problem.constraints.append(UnaryConstraint(letter, lambda x: x != 1))
    #         #   # Constraint: Sum of two variables before the last one from the left must be greater than 9
    #         # second_last_letter_RHS = LHS0[0] 
    #         # third_last_letter_RHS = LHS1[0] 
    #         # problem.constraints.append(
    #         #     BinaryConstraint(
    #         #         (third_last_letter_RHS, second_last_letter_RHS),
    #         #         lambda x, y: x + y > 9
    #         #     )
    #         # )
    #     max_len = max(len(LHS0), len(LHS1), len(RHS))
    #     for i in range(max_len - 1, -1, -1):
    #         z = RHS[i]  
    #         if i < len(LHS0) and i < len(LHS1):
    #                x = LHS0[i]
    #                y = LHS1[i]
    #                xy=x+y
    #                problem.constraints.append(BinaryConstraint((xy, z),lambda xy, z: xy == z))
    #         elif i < len(LHS0):
    #                 x = LHS0[i]
    #                 problem.constraints.append(BinaryConstraint((x, z),lambda x, z: x == z))
    #         elif i < len(LHS1):
    #             y = LHS1[i]
    #             problem.constraints.append(BinaryConstraint((y, z),lambda y, z: y == z))   
    #     return problem