import numpy as np
import random
import os

# Maze size variables

rows = 20
cols = 20

# Maze initialization
maze = np.zeros((rows, cols))  # Zeros are walls

start_val = 8  # Starting point
end_val = 5  # Ending point
player_val = 9  # Player position

# Randomly pick starting and ending points
start_row = rows - 1
start_col = random.randint(1, cols - 2)

end_row = 0
end_col = random.randint(1, cols - 2)

# Arbitrary numbers assigned to the starting and ending point
maze[start_row][start_col] = start_val
maze[end_row][end_col] = end_val

# Global variables
pathCoords = []


# Functions required:
# 1. Path generator
# 2. Branch generator
# 3. Reset function
# 4. Maze update
# 5. Maze to string to print the maze for debugging

def pathGen():
    global pathCoords
    global start_row, start_col
    global end_row, end_col
    global rows, cols
    global maze


    # Store various values in variables
    startCoords = [start_row - 1, start_col]
    endCoords = [end_row + 1, end_col]
    currentCoords = startCoords

    # Movement functions
    def moveUp():
        if currentCoords[0] - 1 > 0:
            currentCoords[0] -= 1

    def moveDown():
        if currentCoords[0] + 1 < rows:
            currentCoords[0] += 1

    def moveLeft():
        if currentCoords[1] - 1 > 0:
            currentCoords[1] -= 1

    def moveRight():
        if currentCoords[1] + 1 < cols:
            currentCoords[1] += 1

    # Create a random path

    while currentCoords != endCoords and len(pathCoords) < int((rows/2)+(cols/2)):

        ch = random.randint(0, 3)
        if ch == 0:
            moveUp()
        elif ch == 1:
            moveDown()
        elif ch == 2:
            moveLeft()
        elif ch == 3:
            moveRight()

        pathCoords.append(tuple(currentCoords))

    rowsRequired = currentCoords[0] - end_row - 1
    colsRequired = currentCoords[1] - end_col

    # Get to the end point directly
    while rowsRequired != 0:
        pathCoords.append(tuple([pathCoords[-1][0] - 1, pathCoords[-1][1]]))
        rowsRequired -= 1

    while colsRequired != 0:
        if colsRequired > 0:
            pathCoords.append(tuple([pathCoords[-1][0], pathCoords[-1][1] - 1]))
            colsRequired -= 1
        elif colsRequired < 0:
            pathCoords.append(tuple([pathCoords[-1][0], pathCoords[-1][1] + 1]))
            colsRequired += 1

    # Incorporate it into the maze

    for RxC in pathCoords:
        maze[RxC[0]][RxC[1]] = 1


def branchGen(noOfBranches):

    # Movement functions
    def moveUp(currentCoords):
        global maze
        if currentCoords[0] - 1 > 0:
            currentCoords[0] -= 1
            maze[currentCoords[0]][currentCoords[1]] = 1

    def moveDown(currentCoords):
        global maze
        if currentCoords[0] + 1 < rows:
            currentCoords[0] += 1
            maze[currentCoords[0]][currentCoords[1]] = 1

    def moveLeft(currentCoords):
        global maze
        if currentCoords[1] - 1 > 0:
            currentCoords[1] -= 1
            maze[currentCoords[0]][currentCoords[1]] = 1

    def moveRight(currentCoords):
        global maze
        if currentCoords[1] + 1 < cols:
            currentCoords[1] += 1
            maze[currentCoords[0]][currentCoords[1]] = 1

    for branch in range(noOfBranches):
        node = random.choice(pathCoords[1:-2])
        prev = pathCoords[pathCoords.index(node)-1]
        next = pathCoords[pathCoords.index(node)+1]

        # 1. Pick any directions besides the two that are already part of the path
        prevDir = [node[0] - prev[0], node[1] - prev[1]]  # One item will be 0, the other will be +1 or -1
        nextDir = [next[0] - node[0], next[1] - node[1]]  # The 0 will have the same index in both arrays unless node is a turning poi
        # 2. Randomly move in the decided direction for maybe a quarter of the no of cols

        branchLength = int((rows+cols)/2)
        for i in range(branchLength):
            # Move in any direction except backwards
            # Check every block around node and recognize the other 1s
                           #    moveUP()                moveDown()            moveRight()              moveLeft()
            neighbors = [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1] + 1), (node[0], node[1] - 1)]
            corrFuncs = ["up", "down", "left", "right"]

            try:
                ch = random.choice(corrFuncs)
                if ch == "up":
                    noOfSquares = random.randint(1, node[0] - end_row - 1)
                    for j in range(noOfSquares):
                        moveUp(list(node))

                elif ch == "down":
                    noOfSquares = random.randint(1, node[0] - end_row - 1)
                    for j in range(noOfSquares):
                        moveDown(list(node))

                elif ch == "left":
                    noOfSquares = random.randint(1, node[0] - end_row - 1)
                    for j in range(noOfSquares):
                        moveLeft(list(node))

                elif ch == "right":
                    noOfSquares = random.randint(1, node[0] - end_row - 1)
                    for j in range(noOfSquares):
                        moveRight(list(node))
            except IndexError:
                continue

            except ValueError:
                continue

        # 3. Add at least 1 turn which goes upwards
        moveUp(list(node))


def reset():

    global rows, cols, maze

    # Save player position, end position and start position
    playerRow = None
    playerCol = None

    for row in range(len(maze)):
        for cell in range(len(maze[row])):
            if maze[row][cell] == player_val:

                playerRow = row
                playerCol = cell

    maze = np.zeros((rows, cols))
    maze[playerRow][playerCol] = player_val


def maintainBorderWalls():
    # Side walls
    for r in maze:  # For each row in the maze
        if r[0] != start_val and r[0] != end_val:
            r[0] = 0  # Make the first and last element of each row a wall

        if r[-1] != start_val and r[-1] != end_val:
            r[-1] = 0

    # Top and bottom walls
    for cellNo in range(len(maze[0])):  # For each cell in the upper boundary of the maze
        if maze[0][cellNo] == 1:
            maze[0][cellNo] = 0

    for cellNo in range(len(maze[-1])):
        if maze[-1][cellNo] == 1:
            maze[-1][cellNo] = 0


def updateMaze(move):
    global player_row
    global player_col
    global maze

    maze[player_row][player_col] = 1
    if move == 'w':
        if maze[player_row - 1][player_col] != 0:
            player_row -= 1
        else:
            print(f'{"Invalid Move"}')
    elif move == 's':
        if maze[player_row + 1][player_col] != 0:
            player_row += 1
        else:
            print(f'{"Invalid Move"}')
    elif move == 'a':
        if maze[player_row][player_col - 1] != 0:
            player_col -= 1
        else:
            print(f'{"Invalid Move"}')
    elif move == 'd':
        if maze[player_row][player_col + 1] != 0:
            player_col += 1
        else:
            print(f'{"Invalid Move"}')

    else:
        print(f'{"Invalid move"}')

    if player_row + player_col != 0 and player_col != 0 and player_col != len(maze[0]):
        maze[player_row][player_col] = 9
        return maze


# Number-Symbol
ones = '__'
zeros = '##'
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
            elif int(cell) == 1:
                maze_str += ones
            elif int(cell) == start_val:
                maze_str += start_pt
            elif int(cell) == end_val:
                maze_str += end_pt
            elif int(cell) == player_val:
                maze_str += player
        maze_str += "\n"
    return maze_str


player_row, player_col = start_row, start_col

counter = 0

pathGen()
branchGen(10)
maintainBorderWalls()
while (player_row, player_col) != (end_row, end_col):

    maze[start_row][start_col] = start_val
    maze[end_row][end_col] = end_val

    print(mazeToString(maze))
    move = input('').lower().strip()
    maze = updateMaze(move)
    os.system('cls')
    counter += 1

if player_row == end_row and player_col == end_col:
    print('Maze completed!!')