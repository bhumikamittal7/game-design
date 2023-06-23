import numpy as np
import random
from colorama import Fore
# update move on maze as the key pressed.
def updatemaze (move):
    if move == "left":
        if start[1] != 0:
            if maze[start[0], start[1] - 1] != 1:
                start[1] = start[1] - 1
                maze[start[0], start[1] + 1] = 0
                maze[start[0], start[1]] = 8
    if move == "right":
        if start[1] != 9:
            if maze[start[0], start[1] + 1] != 1:
                start[1] = start[1] + 1
                maze[start[0], start[1] - 1] = 0
                maze[start[0], start[1]] = 8
    if move == "down":
        if start[0] != 9:
            if maze[start[0] + 1, start[1]] != 1:
                start[0] = start[0] + 1
                maze[start[0] - 1, start[1]] = 0
                maze[start[0], start[1]] = 8
    if move == "up":
        if start[0] != 0:
            if maze[start[0] - 1, start[1]] != 1:
                start[0] = start[0] - 1
                maze[start[0] + 1, start[1]] = 0
                maze[start[0], start[1]] = 8
    return maze


# till we have entries of 0 and 1. Let's replace them with XX and __
def print_maze(maze):
# access each element of maze.
    for i in range(0, 10):
        for j in range(0, 10):
# if its 0 means free space Replace it with __
            if maze[i][j] == 0:
                print(Fore.GREEN, f'{"__"}', end='')
# 1 means walls. Replace it with XX.
            elif maze[i][j] == 1:
                print(Fore.RED, f'{"XX"}', end="")
# 8 means start point. Replace it with @@.
            elif maze[i][j] == 8:
                print(Fore.WHITE, f'{"@@"}', end="")
# 5 means end point. Replace it with ^^
            elif maze[i][j] == 5:
                print(Fore.BLUE, f'{"^^"}', end="")
        print()

# first initialize maze with all 0 entries. we will modify later.
maze = np.zeros(shape=(10, 10))
# print_maze(maze)
# how to access each element of matrix.
for i in range(0, 10):
    for j in range(0, 10):
# since we will choose the walls to be random. how to write logic ?
         if random.randint(0, 4) > 1:
            maze[i][j] = 1
# print (maze)
# ------------------------------------------
# get start point
# we have 10X10 Maze. So for start we need to choose any 8 out of 10 columns.
# similarly for end points.
randomstart = random.randint(1, 8)
randomend = random.randint(1, 8)
# after getting the random column we need to get actual position of start and end.
start = np.array([0, randomstart])
end = np.array([9, randomend])
# check if start and end is correct.
print("start point is :", start)
print("end point is : ", end)
# start to be denoted as 8.
# end to be denoted as 5.
maze[start[0], start[1]] = 8
maze[end[0], end[1]] = 5
print_maze(maze)
# ----------------------------------------
# let's discover what are the adjacent walls of current cell.
def adjacentcells(current):
#let have an empty list.. where u will push the adjacent of current cell.
    walls=[]
    if current[0] == end[0]-1:
        if current[0] - 1 > 0 and current[1] > 0:
            walls.append([current[0] - 1, current[1]])
    if current[0] > 0 and current[1]-1 > 0 and current[1]-1 != 0:
        walls.append([current[0], current[1]-1])
    if current[0]+1 < 10 and current[0]+1 != 9 and current[1] > 0:
        walls.append([current[0]+1, current[1]])
    if current[0] > 0 and current[1]+1 < 10 and current[1]+1 != 9:
        walls.append([current[0], current[1]+1])

    return walls
# before starting the loop let's make a current variable to keep track of position we are currently in.
current = start
# also tracking the position for previous cell.
previous = current
while current[0] != end[0]-1 or current[1] != end[1]:
    walls = adjacentcells(current)
    randomcell = previous
    while randomcell[0] == previous[0] and randomcell[1] == previous[1]:
        randomno = random.randint(0, len(walls)-1)
        randomcell = walls[randomno]
    maze[randomcell[0]][randomcell[1]] = 0
    previous = current
    current = randomcell

# -------------for boundary--------
# at the outer edges there should be boundary like a square.
for i in range(0,10):
    maze[i, 0] = 1
    maze[i, 9] = 1
# remember there is a random start and end point at the periphery. Don't make them walls.
    if i != start[1]:
        maze[0][i] = 1
    if i != end[1]:
        maze[9, i] = 1


# -------------------------------------------
# adding loops for continuously getting the user input.
while chr!= "x" or (start[0] != end[0] and start[1] != end[1]):
    print("")
# ask user for a s d w keys ?
    chr = input("enter a s d w for left down right up movement respectively ")
# if pressed key = some value, you need to update the maze.
    if (chr == "a") or (chr == "A"):
        print("move left - decrement col ")
        maze = updatemaze("left")
    elif (chr == "d") or (chr == "D"):
        print("mov right - increment col ")
        maze = updatemaze("right")
    elif (chr == "s") or (chr == "S"):
        print("move down - decrement row ")
        maze = updatemaze("down")
    elif (chr == "w") or (chr == "W"):
        print("move up - increment row ")
        maze = updatemaze("up")
# let's have a cancel button to exit the maze in between.
    elif (chr == "x") or (chr == "X"):
        break
# if someone pressed other than a s d w and x then??
    else:
        print("invalid move dont do anything ")

    print_maze(maze)

# just a display message if you reach the end points.
    if start[0] == end[0] and start[1] == end[1]:
        print("")
        print("yayyyy!! you won The Game")
        break