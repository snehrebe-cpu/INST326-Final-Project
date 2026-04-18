"""
A template for a python script deliverable for INST326.
Driver: Your Name
Navigator: Partner Name (if any)
Assignment: Rock Paper Scissors
Date: 02_06_26
Challenges Encountered: None
"""

import sys
import argparse
import os

def determine_winner(p1, p2):
    """
    Determine the winner of a Rock-Paper-Scissors round.

    Args:
        p1 (str): Player 1 choice ('r', 'p', or 's')
        p2 (str): Player 2 choice ('r', 'p', or 's')

    Returns:
        str: 'player1', 'player2', or 'tie'
    """

    # Tie case
    if p1 == p2:
        return "tie"

    # Player 1 winning cases
    if (p1 == "r" and p2 == "s") or \
       (p1 == "s" and p2 == "p") or \
       (p1 == "p" and p2 == "r"):
        return "player1"

    # Otherwise player 2 wins
    return "player2"
pass

def main(player1_name, player2_name):
    """
    Run the Rock-Paper-Scissors game.

    Args:
        player1_name (str): Name of player 1
        player2_name (str): Name of player 2
    """
    
    # Get inputs
    p1 = input("Enter player 1's hand shape ('r', 'p', or 's'): ").lower()
    os.system('cls||clear')

    p2 = input("Enter player 2's hand shape ('r', 'p', or 's'): ").lower()
    os.system('cls||clear')

    # Determine winner
    result = determine_winner(p1, p2)

    # Print result
    if result == "tie":
        print("Tie!")
    elif result == "player1":
        print(f"{player1_name} wins!")
    else:
        print(f"{player2_name} wins!")
        
pass

def parse_args(args_list):
    """
    Parse command line arguments.

    Args:
        args_list (list): List of command line arguments

    Returns:
        args: Parsed arguments object
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'p1_name',
        type=str,
        help="Please enter Player1's Name"
    )

    parser.add_argument(
        'p2_name',
        type=str,
        help="Please enter Player2's Name"
    )

    args = parser.parse_args(args_list)
    return args

if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:])
    main(arguments.p1_name, arguments.p2_name)