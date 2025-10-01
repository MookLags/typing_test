'''
Terminal Typing Test
I made this because I like to spend time on Monkeytype @ https://monkeytype.com and sometimes I am either
without internet or my CPU is taking a beating, causing a lag in the typing test. I wanted to make a lightweight
typing test that ran in the terminal, so I gave it a shot. I found the get_input function on a medium blog
post (I can't find it anymore!), everything else if of my own design. 

Currently working on:
 - Generating typed chars overtop of the string of random words.

'''

VERSION = '0.1'

### IMPORTS ###

try:
  import termios
  import tty
  import sys
  import random
  import shutil
  import faker
  from colorama import Fore, Back, init
except ImportError as e:
  print(f'Failed to import module: {e}')

# Initialize Faker
fake = faker.Faker()

# Init colorama to handle clean background colors for incorrectly typed chars
init(autoreset=True) 

### Functions ###
def get_input() -> str:
  '''
  Function: get_input
  Returns: Value of typed key
  '''
  filedescriptors = termios.tcgetattr(sys.stdin)
  tty.setcbreak(sys.stdin)
  key = sys.stdin.read(1)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

  return key

def generate_words():
  words = [fake.word() for _ in range(100)]
  words = ' '.join([random.choice(words) for i in range(50)])
  return words

def main_game_loop():
  pass

random_sentence = generate_words()
sentence_length = len(random_sentence)
key_strokes = 0
print(random_sentence)
while key_strokes != sentence_length:
  char_input = get_input()

  if char_input == '\x7f': # Checks if key pressed is backspace
    print('\b \b', end='', flush=True) # and handles accordingly
    key_strokes -= 1
  else: # Checking for any letter character
    if char_input == random_sentence[key_strokes]:
      print(Back.GREEN + char_input, end='', flush=True) # Green if correct
    else:
      print(Back.RED + char_input, end='', flush=True) # Red if incorrect
    key_strokes += 1
print('\n\ngood job!') # Placeholder until I get stats for typing test
