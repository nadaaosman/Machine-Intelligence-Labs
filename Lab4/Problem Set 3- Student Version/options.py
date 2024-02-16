# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
         "noise": 0,   # No action noise, meaning the agent's actions are deterministic
        "discount_factor": 1,   # Full consideration of future rewards, no discounting (gamma = 1)
        "living_reward": -5   # Negative living reward, discouraging the agent from lingering in non-terminal states
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,          # Moderate action noise, allowing some deviation from the intended direction  
        "discount_factor": 0.2,     # Low discount factor, indicating heavy discounting of future rewards (gamma = 0.2)
        "living_reward": -1      # Negative living reward, discouraging the agent from lingering in non-terminal states
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
          "noise": 0,               # No action noise, meaning the agent's actions are deterministic
        "discount_factor": 1.2,       # High discount factor, giving more emphasis to future rewards (gamma = 1.2)
        "living_reward": -5      # Negative living reward, discouraging the agent from lingering in non-terminal states
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,        # Moderate action noise, allowing some deviation from the intended direction       
        "discount_factor": 1.19,     # Slightly higher discount factor, giving more emphasis to future rewards (gamma = 1.19)  
        "living_reward": -2          # Negative living reward, discouraging the agent from lingering in non-terminal states
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,            # No action noise, meaning the agent's actions are deterministic
        "discount_factor": 1,     # High discount factor, giving substantial emphasis to future rewards (gamma = 0.99)
        "living_reward": 20       # Positive living reward, encouraging the agent to stay in non-terminal states
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
         "noise": 0,         # No action noise, meaning the agent's actions are deterministic       
        "discount_factor": 1,    # High discount factor, giving substantial emphasis to future rewards (gamma = 0.99)  
        "living_reward": -20     # Negative living reward, strongly discouraging the agent from staying in non-terminal states
    }