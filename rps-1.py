"""A template for a python script deliverable for INST326.
Driver: Sean Nehrebecky
Navigator: Tinsae Adem
Assignment: Template INST326
Date: 1_24_21
Challenges Encountered: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import sys
import argparse
import os


def determine_winner(p1, p2):
    # insert code and docstrings here
    """ 
    p1(str): P1 choice ('r', 'p' , or 's')
    p2(str); p2 choice ('r', 'p', or 's')

    returns:
        str: 'Player1_name' , 'Player2_name', 'tie'

    """
    if p1 == 'r' and p2 == 's' or \
       p1 == 's' and p2 == 'p' or \
       p1 == 'p' and p2 == 'r':
        return 'player1'
    else:
        return 'player2'


def main(player1_name, player2_name):
    # insert code and docstrings here
    """ Runs one round of Rock-Paper-Scissors using user input. 

    Args: 
         player1_name (str): Name of Player 1 
         player2_name (str): Name of Player 2 
     """
    p1 = input("Enter player 1's hand shape ('r', 'p', or 's'):\n")
    os.system('cls||clear')

    p2 = input("Enter player 2's hand shape ('r', 'p', or 's'):\n")
    os.system('cls||clear')

    result = determine_winner(p1, p2)
    if result == 'tie':
        print("Tie!")
    elif result == 'player1':
        print(f"{player1_name} wins!")
    else:
        print(f"{player2_name} wins!")


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments 
    Args:
    args_list (list) : the list of strings from the command prompt
    Returns:
    args (ArgumentParser)
    """
    # For the sake of readability it is important to insert comments all throughout.
    # Complicated operations get a few lines of comments before the operations
# commence.
    # Non-obvious ones get comments at the end of the line.
    # For example:
    # This function uses the argparse module in order to parse command line
# arguments.

    parser = argparse.ArgumentParser()  # Create an ArgumentParser object.

    # Then we will add arguments to this parser object.
    # In this case, we have a required positional argument.
    # Followed by an optional keyword argument which contains a default value.
    parser.add_argument('p1_name', type=str,
                        help="Please enter Player1's Name")
    parser.add_argument('p2_name', type=str,
                        help="Please enter Player2's Name")

    # We need to parse the list of command line arguments using this object.
    args = parser.parse_args(args_list)

    return args


if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:])  # Pass in the list of command line
    main(arguments.p1_name, arguments.p2_name)