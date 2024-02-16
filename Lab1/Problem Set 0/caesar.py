from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list
'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    text=ciphered.split()
    after_shift=[]
    count_min=None
    shift_value=None
    count=0
    dictionary_set = set(dictionary)
    for shift in range(26):
      for word in text:
          shifted = [chr(((ord(char) - ord('a') - shift) % 26) + ord('a')) for char in word]
          shifted=''.join(shifted)
          if shifted not in dictionary_set:
                count += 1
          after_shift.append(shifted)
      if count_min is None or count < count_min:
        count_min = count
        shift_value=shift
        deciphere=after_shift
      count=0
      after_shift=[]

    return (' '.join(deciphere),shift_value,count_min)
# print(caesar_dechiper(read_text_file('data/text4_ciphered.txt'), read_word_list('data/english.txt')))
