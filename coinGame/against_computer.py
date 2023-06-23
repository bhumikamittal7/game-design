import random
import numpy as np
#Game Setup
Coin_Array = [random.randint(1,5) for i in range(4)]


# print(Coin_Array)
def againstComputer(Coin_Array):

    turn = 1
    while Coin_Array != [0]*4:
        print("The coin heap is: "+str(Coin_Array))


        if turn%2 == 0:
            tmp = input("Your move\nMove a coins from heap number b. Enter space seperated a and b: \n").split()
            a = int(tmp[0])
            b = int(tmp[1])
        # print(a,b)
            Coin_Array[b-1] = Coin_Array[b-1] - a
        else:
            print("Computer's move")
            options = np.nonzero(Coin_Array)
            # print(options)
            b = random.choice(options[0])
            # print(b)
            a = random.randint(1,Coin_Array[b])
            Coin_Array[b] = Coin_Array[b] - a
            b = b+1
            print("Computer removed "+str(a)+" coin(s) from heap number "+str(b))

        turn= turn+1
        print("\n")

    if turn%2 == 1:
        print("You are the winner")
    else:
        print("Computer is the winner")