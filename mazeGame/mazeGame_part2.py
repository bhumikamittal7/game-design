
# till we have entries of 0 and 1. Let's replace them with XX and __
#replace 8 with @@ and 5 with ^^
#the idea is to go over all the entries in the matrix and check if they are 1, 0, 8 or 5 and do the replacement accordingly
def print_maze(maze):
    #code here for print


# ----------------------------------------------------------------------------------------------
# adding loops for continuously getting the user input
#accept input until we win the game or the user inputs the cancel command
#complete the loop here
while ( ):
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


# ------------------------------------------------------------------------------------------------

    # now let's write the update function
#this moves the start point on maze as the key pressed
#I am giving you the logic for left movement - read it and try to understand the same
#Also explain the logic in words using comments

    def updatemaze(move):
        if move == "left":
            if start[1] != 0:
                if maze[start[0], start[1] - 1] != 1:
                    start[1] = start[1] - 1
                    maze[start[0], start[1] + 1] = 0
                    maze[start[0], start[1]] = 8
        if move == "right": #write the same for right movement - this is easy since you have one for left

        if move == "down":  #write the logic for down, thing about this in coordinates, of left right is on x axis, this is y axis

        if move == "up":    #write one for up as well, should be easy (Ik you all are smart)

        return maze

