import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    if(string==' '):
       return True
    else: 
      reversed_string = string[::-1]
      if(string==reversed_string):
         return True
      else: 
         return False

    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
