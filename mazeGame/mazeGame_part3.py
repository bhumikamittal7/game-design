# let's discover what are the adjacent walls of current cell.
def adjacentcells(current):
#let have an empty list.. where u will push the adjacent of current cell row and column.
    walls=[]
# we will check if the row has reached index 9. If that's the case we will move just left and right to get same
# column as endpoint.
    if current[0] == end[0]-1:
        #if u want to move up then check row should not be less than 0 and column should be positive.
            walls.append([current[0] - 1, current[1]])
    # if ur row is currently positive and u want to move left then check row should be greater than 0.
            walls.append([current[0], current[1]-1])
    # if u want to move right check it will not exceed index 9.
            walls.append([current[0]+1, current[1]])
    # if u want to move down check it not exceed the row no. 9 .
            walls.append([current[0], current[1]+1])

    return walls

# -----------------------------------------------------------------------------------------------------------
# before starting the loop let's make a current variable to keep track of position we are currently in.
# also track the position for previous cell.
current =
previous =

# -----------------------------------------------------------------------------------------------------------

# run a loop till u reach (9,end[1])
while ( ):
    walls = adjacentcells(current)
    randomcell = previous
    # choose the wall randomly till u get previous cell and next randomcell the same
    while ( ):
        randomno = random.randint(0, len(walls)-1)
        randomcell = walls[randomno]
    # make the current randomcell to be wakable area 0.
    #update the rule.
    previous = current
    current = randomcell

# -----------------------------------------------------------------------------------------------------------
    # just a display message if you reach the end points. Think about the condition for the end point..
#you have to fill the conditions in the if statement given below
    if ( ):
        print("")
        print("yayyyy!! you won The Game")
        break