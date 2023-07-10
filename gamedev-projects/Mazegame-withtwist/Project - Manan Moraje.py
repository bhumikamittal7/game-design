import numpy as np
import random
import os
from colorama import Fore

# Decide the size of the maze
rows = 4
cols = 4


# wall_val = 1
start_val = 8
end_val = 5
player_val = 9

# Initialize an empty maze
maze = np.zeros((rows, cols))

# Randomly pick starting and ending points
start_row = rows-1
start_col = random.randint(1, cols-2)

end_row = 0
end_col = random.randint(1, cols-2)

# Arbitrary numbers assigned to the starting and ending point
maze[start_row][start_col] = start_val
maze[end_row][end_col] = end_val


# Start adding walls
def isSolvable(cR, cC):
    global maze

    if maze[cR-1][cC] == 1 and maze[cR][cC - 1] == 1 and maze[cR][cC + 1] == 1:
        ch = random.randint(0, 2)
        if (cR-1) != 0 and (cC - 1) != 0 and (cC + 1) != len(maze[0])-1:
            if ch == 0:
                maze[cR-1][cC] = 0
                cR -= 1
            elif ch == 1:
                maze[cR][cC - 1] = 0
                cC -= 1
            else:
                maze[cR][cC + 1] = 0
                cC += 1

        elif (cR-1) == 0 and (cC - 1) != 0 and (cC + 1) != len(maze[0])-1:
            ch = random.randint(1, 2)
            if ch == 1:
                maze[cR][cC - 1] = 0
                cC -= 1
            else:
                maze[cR][cC + 1] = 0
                cC += 1

        elif (cR-1) != 0 and (cC - 1) == 0 and (cC + 1) != len(maze[0])-1:
            ch = random.randint(0, 1)
            if ch == 0:
                maze[cR-1][cC] = 0
                cR -= 1
            else:
                maze[cR][cC + 1] = 0
                cC += 1

        elif (cR-1) != 0 and (cC - 1) != 0 and (cC + 1) == len(maze[0])-1:
            ch = random.randint(0, 1)
            if ch == 0:
                maze[cR-1][cC] = 0
                cR -= 1
            elif ch == 1:
                maze[cR][cC - 1] = 0
                cC -= 1



def createWalls():
    global maze

    walls = []

    # Boundary walls

    # Save player position (if there is one)
    pR = 0
    pC = 0
    for row in range(len(maze)):
        for cell in range(row):
            if maze[row][cell] == player_val:
                pR = row
                pC = cell

    # Side walls
    for r in maze:  # For each row in the maze
        if r[0] != start_val and r[0] != end_val:
            r[0] = 1  # Make the first and last element of each row a wall

        if r[-1] != start_val and r[-1] != end_val:
            r[-1] = 1

    # Top and bottom walls
    for cellNo in range(len(maze[0])):  # For each cell in the upper boundary of the maze
        if maze[0][cellNo] == 0:
            maze[0][cellNo] = 1

    for cellNo in range(len(maze[-1])):
        if maze[-1][cellNo] == 0:
            maze[-1][cellNo] = 1

    # Random walls by quadrant

    for i in range(random.randint(int(rows*cols/16), int(rows*cols/12))):
        column = random.randint(1, int(cols/2))  # Col 1 to len/4
        row = random.randint(1, int(rows/2))

        maze[column][row] = 1

    for i in range(random.randint(int(rows*cols/16), int(rows*cols/12))):
        column = random.randint(int(cols/2), int(cols-1))  # len/4 to len/2
        row = random.randint(1, int(rows/2))

        maze[column][row] = 1

    for i in range(random.randint(int(rows*cols/16), int(rows*cols/12))):
        column = random.randint(1, int(cols/2))  # len/2 to 3*len/4
        row = random.randint(int(rows/2), int(rows-1))

        maze[column][row] = 1

    for i in range(random.randint(int(rows*cols/16), int(rows*cols/12))):
        column = random.randint(int(cols/2), int(cols-1))  # 3*len/4 to len
        row = random.randint(int(rows/2), int(rows-1))

        maze[column][row] = 1

    # Make sure there's a gap in the center of the maze

    # Make sure maze is solvable

    # Loop through the maze, if the walls are adjacent to the end or starting point, delete them and a random wall next to them (if any)

    for r in range(len(maze)):
        for cell in range(len(maze[r])):
            if maze[r][cell] == 1:
                if r != 0 and r < len(maze) - 1:
                    if maze[r-1][cell] == end_val:
                        maze[r][cell] = 0
                    elif maze[r+1][cell] == start_val:
                        maze[r][cell] = 0

    if pR + pC != 0:
        maze[pR][pC] = player_val
        isSolvable(pR, pC)


def removeWalls():
    global maze
    for row in range(len(maze)):
        for cell in range(row):
            if maze[row][cell] == 1:
                maze[row][cell] = 0


# Number-Symbol
zeros = '  '
ones = '##'
start_pt = '^^'
end_pt = '><'
player = '()'


def mazeToString(mazeVar):
    maze_str = "\n"
    # Convert the maze into a printable string
    for R in mazeVar:  # For each row in the maze
        for cell in R:  # For each cell in the row
            if int(cell) == 0:
                maze_str += zeros
                #print(zeros, end='')
            elif int(cell) == 1:
                maze_str += ones
                #print(Fore.RED, f'{ones}', end='')
            elif int(cell) == start_val:
                maze_str += start_pt
                #print(Fore.BLUE, f'{start_pt}', end='')
            elif int(cell) == end_val:
                maze_str += end_pt
                #print(Fore.YELLOW, f'{end_pt}', end='')
            elif int(cell) == player_val:
                maze_str += player
        maze_str += "\n"
        # print()
    return maze_str


player_row, player_col = start_row, start_col


def updateMaze(move):
    global player_row
    global player_col
    global maze

    oldpR = player_row
    oldpC = player_col

    maze[player_row][player_col] = 0
    if move == 'w':
        if maze[player_row - 1][player_col] != 1:
            player_row -= 1
        else:
            print(Fore.RED, f'{"Invalid Move"}')
    elif move == 's':
        if maze[player_row + 1][player_col] != 1:
            player_row += 1
        else:
            print(Fore.RED, f'{"Invalid Move"}')
    elif move == 'a':
        if maze[player_row][player_col - 1] != 1:
            player_col -= 1
        else:
            print(Fore.RED, f'{"Invalid Move"}')
    elif move == 'd':
        if maze[player_row][player_col + 1] != 1:
            player_col += 1
        else:
            print(Fore.RED, f'{"Invalid Move"}')

    else:
        print(Fore.RED, f'{"Invalid move"}')

    if player_row + player_col != 0 and player_col != 0 and player_col != len(maze[0]):
        print(Fore.RESET, f"{''}", end='')
        maze[player_row][player_col] = 9
        return maze


counter = 0
while (player_row, player_col) != (end_row, end_col):

    if counter % 2 == 0:
        removeWalls()
        createWalls()
    print(mazeToString(maze))

    move = input('').lower().strip()

    updateMaze(move)
    os.system('cls')
    counter += 1

if player_row == end_row and player_col == end_col:
    print(Fore.YELLOW, f'{"Maze completed!!"}')
    print(Fore.RESET, f"{''}", end='')