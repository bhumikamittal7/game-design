#import functions - numpy, random and colorama
import numpy as np
import random
from colorama import Fore
# ------------------------------------------------------------------------------

# first initialize maze with all 0 entries.
maze =
# print_maze(maze)

# Access each element of matrix and make random walls


# ------------------------------------------------------------------------------
# get start point. we have 10X10 Maze. So for start we need to choose any 8 out of 10 columns.
# similarly for end points.
randomstart =
randomend =

# after getting the random column we need to get actual position of start and end.
start =
end =

# check if start and end is correct.
print("start point is :", start)
print("end point is : ", end)

# start to be denoted as 8. end to be denoted as 5.
#you can use any other distinct number, 8 and 5 are just examples


# -------------for boundary-----------------------------------------------------
# at the outer edges there should be boundary like a square.


# remember there is a random start and end point at the periphery. Don't make them walls.

