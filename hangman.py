"""
Jatin Gandhi., 
Classic hangman game of guessing., 
NOTE: TODO: Improve logic for repeat characters
"""
import random;
import os;

HANGMANPICS = [r'''
  +---+
  |   |
      |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

#Word bank of animals
words = ('ant baboon badger bat bear beaver camel cat clam cobra cougar '
        'coyote crow deer dog donkey duck eagle ferret fox frog goat '
        'goose hawk lion lizard llama mole monkey moose mouse mule newt '
        'otter owl panda parrot pigeon python rabbit ram rat raven '
        'rhino salmon seal shark sheep skunk sloth snake spider '
        'stork swan tiger toad trout turkey turtle weasel whale wolf '
        'wombat zebra ').split()

def showGreetings():
    print("Welcome to Hangman\n");
    print("Guess the animal name", end="");
    print(" out of {0}".format(words)); # For debug only.,
    print("\n");

choosen_word = random.choice(words);
CHOOSEN_WORD = choosen_word;
NUM_CHARACTERS = len(choosen_word);
NUM_GUESS_ALLOWED = NUM_CHARACTERS + 3;
total_char_entered = 0;
current_state = 0;
display_word = ["_"] * len(choosen_word);

# only 'a' to 'z' are valid char., 
valid_chars = [chr(ch) for ch in range(ord('a'), ord('z') + 1)];

def processNextChar():
    global current_state;
    global choosen_word;
    global display_word;
    global total_char_entered;
    # We already reached the limit.,
    if (not "_" in display_word):
        # All words replced., 
        return;

    ch = input("Enter Character: ");

    # if more than one characters are entered or it is not in valid range., 
    # return to main and ask again., 
    if len(ch) > 1 or ch not in valid_chars:
        # print error if required.,
        return;

    total_char_entered = total_char_entered + 1;
    index = choosen_word.find(ch);
    
    if (index == -1):
        current_state += 1;
        print(HANGMANPICS[current_state])
    else:
        display_word[index] = ch;
        choosen_word = choosen_word.replace(ch,'_', 1); # We need to destroy the given character
        print(display_word);
        #print(choosen_word); # Debug only
    
def clear_screen():
    """Clears the console screen."""
    # Check the operating system
    if os.name == 'nt':
        # 'nt' is the name used for Windows
        os.system('cls')
    else:
        # 'posix' is the name used for Unix-based systems (macOS and Linux)
        os.system('clear')

def main():
    global display_word;
    global current_state;
    global total_char_entered;
    global CHOOSEN_WORD;
    global NUM_CHARACTERS;
    global NUM_GUESS_ALLOWED;


    # Debug only 
    # global choosen_word;
    # print(choosen_word);

    current_state = 0;
    showGreetings();
    print(display_word);
    while True:
        processNextChar();

        if (current_state == (len(HANGMANPICS) - 1)):
            print("Person Hanged, you loose!!\n")
            break;
        elif (NUM_CHARACTERS == total_char_entered):
            if(0 == current_state):
                print("You Win!!\n")
                break;
            else:
                continue;
        elif (total_char_entered >= NUM_GUESS_ALLOWED):
            # if current_state < (len(HANGMANPICS)))
            print("You run out of guess., You loose\n");
            break;
        elif ( "".join(display_word) == CHOOSEN_WORD):
            print("You guessed it right, You Win!!\n")
            break;
        else:
            continue;

    
if __name__ == "__main__":
    main();
