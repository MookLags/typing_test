'''
Terminal Typing Test
I made this because I like to spend time on Monkeytype @ https://monkeytype.com and sometimes I am either
without internet or my CPU is taking a beating, causing a lag in the typing test. I wanted to make a lightweight
typing test that ran in the terminal, so I gave it a shot. I found the get_input function on a medium blog
post (I can't find it anymore!), everything else if of my own design. 

Currently working on:
 - Adding stats for typing test (time take, wpm)
  - Bonus: Add these stats to a sqlite database and have an option to view
'''

VERSION = '0.1'

### IMPORTS ###

try:
  import math
  import termios
  import tty
  import os
  import sys
  import random
  import faker
  from colorama import Fore, Back, init
except ImportError as e:
  print(f'Failed to import module: {e}')
  sys.exit(2)

# Initialize Faker
fake = faker.Faker()

# Init colorama to handle clean background colors for incorrectly typed chars
init(autoreset=True) 

# Get terminal width
terminal_width = os.get_terminal_size().columns

### Functions ###
def terminate():
  print('Exiting game...')
  sys.exit(0)

def get_input() -> str:
  '''
  Function: get_input
  Returns: Value of typed key
  Uses: Used in main_game_loop to get typed char and compare with expected char
  '''
  filedescriptors = termios.tcgetattr(sys.stdin)
  tty.setcbreak(sys.stdin)
  key = sys.stdin.read(1)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

  return key

def generate_words():
  '''
  Function: generate_words
  Returns: str of words randomly generated with Faker module
  Uses: Used in main_game_loop to create the taget words to type
  '''
  words = [fake.word() for _ in range(100)]
  words = ' '.join([random.choice(words) for i in range(50)])
  return words

def main_game_loop():
  '''
  Function: main_game_loop
  Returns: void
  Uses: __main__ Begins game
  '''
  running = True
  while running:
    random_sentence = generate_words()
    lines_spanned = math.ceil(len(random_sentence) / terminal_width)
    sentence_length = len(random_sentence)
    key_strokes = 0
    print(random_sentence, flush=True, end='')
    print(f"\x1b[{lines_spanned - 1}A\r", end='')
    while key_strokes != sentence_length:
      char_input = get_input()

      if char_input == '\x7f': # Checks if key pressed is backspace
        replacement_char = random_sentence[key_strokes - 1]
        print(f'\b{replacement_char}\b', end='', flush=True) # and handles accordingly
        key_strokes -= 1
        
      else: # Checking for any letter character
        if char_input == random_sentence[key_strokes]:
          print(Back.GREEN + char_input, end='', flush=True) # Green if correct
        else:
          print(Back.RED + char_input, end='', flush=True) # Red if incorrect
        key_strokes += 1
    print('\ngood job!') # Placeholder until I get stats for typing test

    play_again = input('Go again? Press any key to keep typing, or [n] to stop\n')
    if play_again == 'n':
      terminate()

if __name__ == '__main__':
  main_game_loop()
