"""
Load the contents of the file into the list.


What am I trying to accomplish?

1. Given an input, tell me the list of words that are probable candidates.
2. From that
"""

# Let's filter out the 5 letter words to begin with.

from collections import defaultdict

def get_all_words():
    """
    Return the list of strings in the dictionary
    :return:
    """
    with open('words.txt', 'r') as file:
        data = file.read().rstrip()
    return data.split('\n')

lowercase_letters = "abcdefghijklmnopqrstuvwxyz"

def is_lower_case_word(word):
    """
    Return true if all the letters in x are lowercase alphabets
    :param x:
    :return:
    """
    for a in word:
        if a not in lowercase_letters:
            return False
    return True


def filter_valid_words(list_of_words):
    list_of_words = map(lambda x: x.lower(), list_of_words)

    return [a for a in filter(lambda x: len(x) == 5 and is_lower_case_word(x),
                  list_of_words)]


"""
Am here to solve for wordle.
I should be able to guess the word in the quickest manner possible.
First guess should be to get the most amount of information.
Once the information is fed in,
Make the next guess in such a way that you again get the most amount of 
information.


"""

def word_passes_the_sieve(possible_wordle, sieve):
    # honor all the conditions of the sieve
    # If one of the condition fails, return false.
    for typ, letter, position in sieve:
        if typ == "g":
            cur_flag = (possible_wordle[position - 1] == letter)
        elif typ == 'y':
            cur_flag = (letter in possible_wordle) and (possible_wordle[
                position - 1] != letter)
        else:
            cur_flag = (letter not in possible_wordle)
        if not cur_flag:
            return False
    return True


def update_wordles_sieve(possible_wordles, sieve):
    ret = []
    for possible_wordle in possible_wordles:
        if word_passes_the_sieve(possible_wordle, sieve):
            ret.append(possible_wordle)
    return ret


class PossibleWordles():
    def __init__(self, possible_wordles):
        self.possible_wordles = possible_wordles
        """
        Let's just use the strategy of using the words that have the most 
        character count.
        """
        self.char_count = self.construct_char_count(self.possible_wordles)
        self.ranked_wordles = self.rank_wordles_based_on_count(
            self.possible_wordles, self.char_count)

    @staticmethod
    def rank_wordles_based_on_count(possible_wordles, char_count):
        ranked_wordles = [] # tuple of (score, word)
        """
        Score is the sum of char counts of the unique letters in the word.
        """
        for wordle in possible_wordles:
            score = 0
            for letter in set(wordle):
                score += char_count[letter]
            ranked_wordles.append((score, wordle))
        return sorted(ranked_wordles, key=lambda x: x[0], reverse=True)


    @staticmethod
    def construct_char_count(possible_wordles):
        char_count = defaultdict(int)
        for wordle in possible_wordles:
            for letter in set(wordle):
                char_count[letter] = char_count[letter] + 1
        return char_count

    def get_ranked_wordles(self):
        return self.ranked_wordles


def update_sieve(guess, colours, sieve):
    for i in range(0, 5):
        letter = guess[i]
        colour = colours[i]
        sieve.append((colour, letter, i + 1 if colour != 'b' else 0))

"""
For now what I want is that, given a list of words, what is the best word to guess,
so that I am able to narrow down to the exact word as fast as possible.

The goal is to narrow down the sieve very effeciently.

Effective score of the word should be computed.
The definition of the effective score is that:
 The expected number of words that will be in the list post this guess. The word that has the minimum score is the best guess.
 For a given word the expected number of words that will be in the list post the guess will be as follows:
 1. All I know is that any of the words in the sieve is a probable candidate.
 If the word x is the answer, what is the score of the word y?
 Over all possible combinations, which word reduced the sieve by a lot? Something to think about.
 Wordle isn't adding quite a bit of value at this point in time. But you are pondering over it for some reason.
 
 
 
"""


def main():
    all_words = get_all_words()
    wordles = filter_valid_words(all_words)
    possible_wordles = wordles
    sieve = []  # character to the position or 'y' or 'n'
    while True:
        guess = str(input())
        if guess == "done":
            break
        else:
            colours = str(input())
            update_sieve(guess, colours, sieve)

        possible_wordles = update_wordles_sieve(possible_wordles, sieve)
        wordles_container = PossibleWordles(possible_wordles)
        print("count " + str(len(possible_wordles)))
        ranked_wordles = wordles_container.ranked_wordles
        for i in range(0, min(20, len(ranked_wordles))):
            print(ranked_wordles[i])



main()
