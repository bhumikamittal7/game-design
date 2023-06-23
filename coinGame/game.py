from two_player import twoPlayer
from against_computer import againstComputer
import random
import numpy as np

#Game Setup
Coin_Array = [random.randint(1,5) for i in range(4)]

userChoice = input("Enter 1 to play against another user\nEnter 2 to play against computer:\n")
if userChoice == "1":
    twoPlayer(Coin_Array)
if userChoice == "2":
    againstComputer(Coin_Array)
