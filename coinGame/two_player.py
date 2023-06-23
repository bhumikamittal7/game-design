import random
#Game Setup
Coin_Array = [random.randint(1,5) for i in range(4)]


# print(Coin_Array)

def twoPlayer(Coin_Array):
    turn = 1
    while Coin_Array != [0]*4:
        print("The coin heap is: "+str(Coin_Array))
        i = 1
        if turn%2 == 0:
            i = 2
        tmp = input("PLAYER "+ str(i)+"'s move\nMove a coins from heap number b. Enter space seperated a and b: \n").split()
        a = int(tmp[0])
        b = int(tmp[1])
        # print(a,b)
        Coin_Array[b-1] = Coin_Array[b-1] - a
        turn= turn+1
        print("\n")

    i = 2
    if turn%2 == 0:
        i = 1
    print("\n\nPlayer " +str(i) +" is the winner")