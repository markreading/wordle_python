## @file wordle_game.py

import time as TIME, random, sys, os
from colorama import Fore, Back, Style

class print_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## class for each dictionary that will be needed for this game
class dictionary():
    # upon class initialization, build the dictionary contents
    def __init__(self, file_name):
        self.contents = self.read_file(file_name=file_name) # contents of the dictionary
        self.length = len(self.contents)                    # length of the dictionary

    # function to read a dictionary file and put the contents line by line into a list
    def read_file(self, file_name):
        dictionary = list()
        with open(file_name) as file:
            for line in file:               # for each line in the file
                line = line.strip()         # run preprocessing on it to get rid of weird stuff
                dictionary.append(line)     # add the line to the dictionary list
        return dictionary
    
    # prints out all the info for the dictionary, takes a lot of space.  for debugging
    def print(self):
        print(self.contents)
        print(self.length)

    # get a random word from the dictionary and return it.
    def random_word(self):
        random_num = int(random.random() * wordle_dict.length)
        return self.contents[random_num]
    
    # check to see if a word exists in the dictionary, may be slightly laggy depending on dictionary size
    def exists(self, word):
        for item in self.contents:
            if item == word: # return true if we find the word
                return True
        # if we have passed through the entire dictionary and the word hasnt been found, return false
        return False

## class for each guess to hold its own list of characters and colors for each
class new_guess():
    def __init__(self, guess_string):
        self.characters = list(guess_string)
        self.colors = [None] * wordle.WORD_LENGTH

## class for the game to store all functions and data needed
class game():
    # upon initialization set the answer and other variables
    def __init__(self, answer):
        self.WORD_LENGTH = 5    # changing this value changes the length of the word for which we are playing wordle
        self.MAX_GUESSES = 6    # changing this allows for more guesses
        self.guesses_count = 0
        self.guesses = list()   # list of guesses that will hold the new_guess class
        self.answer = answer
        self.answer_characters = list(answer)
        self.start_time = TIME.time()
        # keyboard to keep track of letters used and what is available
        self.keyboard = {'a': Back.WHITE, 'b': Back.WHITE,  'c': Back.WHITE,  'd': Back.WHITE,  'e': Back.WHITE, 
                           'f': Back.WHITE, 'g': Back.WHITE,  'h': Back.WHITE,  'i': Back.WHITE,  'j': Back.WHITE, 
                           'k': Back.WHITE, 'l': Back.WHITE,  'm': Back.WHITE,  'n': Back.WHITE,  'o': Back.WHITE, 
                           'p': Back.WHITE, 'q': Back.WHITE,  'r': Back.WHITE,  's': Back.WHITE,  't': Back.WHITE, 
                           'u': Back.WHITE, 'v': Back.WHITE,  'w': Back.WHITE,  'x': Back.WHITE,  'y': Back.WHITE, 
                           'z': Back.WHITE}

    # get input from the user and determine what to do with it
    def get_input(self):
        user_input = input()

        # if the user wants help, print the help information
        if user_input == "\help":
            self.print_help()
            return None
        # check to make sure the input word is the right length
        elif len(user_input) != self.WORD_LENGTH:
            print("Please enter a word with " + str(self.WORD_LENGTH) + " letters.")
            return None
        # check to make sure the word is in the dictionary
        elif not full_dict.exists(user_input):
            print("'" + user_input + "' is not a valid word.  Enter another word.")
            return None
        # this function returns the input upon meeting these conditions
        else:
            return user_input

    # process the guess and determine the colors for each letter in the guess
    def process_guess(self, word):
        # create a new object for the guess so we can store its characters and colors
        guess = new_guess(guess_string = word)

        # go through each character in the word
        for n in range(self.WORD_LENGTH):
            # if the n'th character in the guess is found in the answer characters list AND the index of said character
            # in the answers list is equal to the index we are at in the guess (same letter and same index)
            # set the color to green on the keyboard, and for the letter in the guess
            if guess.characters[n] in self.answer_characters and n == self.answer_characters.index(guess.characters[n]):
                guess.colors[n] = Back.GREEN
                self.keyboard[guess.characters[n]] = Back.GREEN
            # if the n'th character in the guess is found in the list (but not in the correct position, because we already handled that above)
            # set the color to yellow in the guess object, and on the keyboard
            # we also check if the letter is not already green, to prevent a double letter overwriting a previous green
            elif guess.characters[n] in self.answer_characters and guess.colors[n] != Back.GREEN:
                guess.colors[n] = Back.YELLOW
                self.keyboard[guess.characters[n]] = Back.YELLOW
            # if we dont find the n'th character in the guess, turn the keyboard and they guess black
            else:
                guess.colors[n] = Back.BLACK
                self.keyboard[guess.characters[n]] = Back.BLACK

        # add the new guess to the list of guesses and increment the guess count
        self.guesses.append(guess)
        self.guesses_count += 1

        # check to see if we have won
        if (word == self.answer):
            return True
        return False

    def print_game(self):
        # clear the terminal window
        os.system('cls' if os.name == 'nt' else 'clear')

        # if we are just beginning the game, print out the welcome text, and how to get help
        if self.guesses_count == 0:
            # Start the game here
            print("Welcome to Wordle. Enter '\help' without quotes for how to play and other information.")
            # print("Full dictionary length : " + str(full_dict.length))
            # print("Wordle dictionary length: " + str(wordle_dict.length))
            print("Enter a " + str(wordle.WORD_LENGTH) + " letter word for your guess.\n")

        # print the title and the guess number that we are on
        print("Python Wordle - Guess #" + str(self.guesses_count + 1))

        # print the keyboard, show what keys are available and which are not found in the answer
        print(Style.RESET_ALL + "Available letters:")
        for key, value in self.keyboard.items():
            print(value + key + Back.WHITE + " ", end="")
            
        # make sure to reset the style after printing the keyboard
        print(Style.RESET_ALL)

        # print out each guess one at a time, one per line
        for guess in self.guesses:
            print(Style.RESET_ALL, end="") # clear any style changes, make sure we are on default text
            for n in range(wordle.WORD_LENGTH):
                # print out each letter of the guess, with the coloring associated with it
                # include the end = '' so we dont go to a new line after each letter
                print(guess.colors[n] + guess.characters[n] + Style.RESET_ALL, end="")
            print() # newline after we are done with each guess
        
    # function that prints out the help information
    def print_help(self):
        print("Help Info:")
        print("write later")

## MAIN PROCESS ===============================================================================================

# build wordle dictionary
wordle_dict = dictionary(file_name = "dict_wordle.txt")

# build main dictionary
full_dict = dictionary(file_name = "dict_all_words.txt")

# initialize game and pick a random word for the answer from the wordle dictionary
wordle = game(answer = wordle_dict.random_word())

# print the initial game board
wordle.print_game()

# we go through the loop 6 times because the user gets 6 guesses
while wordle.guesses_count < wordle.MAX_GUESSES:

    # get a user response
    user_input = wordle.get_input()
    # if the users input is not valid, keep getting the input until its ok
    while user_input == None:
        user_input = wordle.get_input()
        
    # once we have a valid guess, we can process it, get the colors of the guess, and update the keyboard
    won = wordle.process_guess(user_input)

    # print the game board once everything has been processed
    wordle.print_game()

    # if we have won, we can break the loop
    if (won):
        break

## The game is now over.  Lets print out the final stats

# get the total time it took the user to play, and convert to minutes and seconds
total_time = TIME.time() - wordle.start_time # time in seconds
minutes = int(total_time / 60)
seconds = int(total_time - minutes * 60)

# print an extra zero if our seconds are less than 10
extra_zero = ""
if seconds < 9:
    extra_zero = "0"

# print out stats and tell the user whether they won or lost
print()
if won:
    print("Congratulations, you won in " + str(wordle.guesses_count) + " guesses!\nTotal Time: " + str(minutes) + ":" + extra_zero + str(seconds) + "\n")
else:
    print("You lose! :(\nThe word was " + wordle.answer + "\nTime used: " + str(minutes) + ":" + extra_zero + str(seconds) + "\n")
