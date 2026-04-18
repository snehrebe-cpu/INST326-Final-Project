from argparse import ArgumentParser
import random 
import sys

SHIP = 6
CAPTIN = 5
CREW = 4

def ask_yn(promt):
    while True: 
        respose = input(promt).lower().strip()[0]
        if response not in{"y", "n"}:
            print("please answer 'y' or 'n'.")
        else: 
            return response == "y"
        
class Player: 
    """A Ship, Captain, Crew Player
        
        Attributes: 
        name (str): the player's name
        ship (bool): weather the player has a ship
        captain (bool): weather the pkayer has a captain 
        crew (bool) weather the pakyer has a crew
        score (bool): the player's score
        """
    def __init__(self, name):
        self.name = name
        self.ship = False
        self.captain = False
        self.crew = False
        self.score = 0
        
    def roll_dice(sef, number=5):
        dice = []
        for i in range(number):
            dice.append(random.randint(1,6))
        return dice

    def take_turn(self):
        print(f"its your turn, {self.name}!")
        dice = self.roll_dice()
        if not self.ship and SHIP in dice:
            self.ship = True
            dice.remove(SHIP)
            print("you got a ship!")
        