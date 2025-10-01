import termios
import tty
import sys
import random
import shutil
import faker
from colorama import Fore, Back, init

fake = faker.Faker()

columns = shutil.get_terminal_size().columns

init(autoreset=True) # init from colorama to handle clean background colors for incorrectly typed chars

def get_input() -> str:
  filedescriptors = termios.tcgetattr(sys.stdin)
  tty.setcbreak(sys.stdin)
  key = sys.stdin.read(1)[0]
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

  return key

words = [fake.word() for _ in range(50)]

random_sentence = ' '.join([random.choice(words) for i in range(50)])
sentence_length = len(random_sentence)
key_strokes = 0
print(random_sentence)
while key_strokes != sentence_length:
  char_input = get_input()
  if char_input == '\x7f':
    print('\b \b', end='', flush=True)
    key_strokes -= 1
  else:
    if char_input == random_sentence[key_strokes]:
      print(Back.GREEN + char_input, end='', flush=True)
    else:
      print(Back.RED + char_input, end='', flush=True)
    key_strokes += 1
print('\n\ngood job!')
