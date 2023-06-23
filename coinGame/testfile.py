Coin_Array = [random.randint(1,5) for i in range(4)]

def twoPlayer(Coin_Array):
    turn = 1
    while Coin_Array != [0]*4:
        print ("the heap is: " + str(Coin_Array))
        i = 1
        if turn%2 == 0:
            i = 2
        tmp = input("PLAYER "+ str(i)+"'s move\nMove a coins from heap number b. Enter space seperated a and b: \n").split()
        print(tmp)
        a = tmp[0]
        b = tmp[1]
        print(a)
        print(b)
        Coin_Array[b-1] = Coin_Array[b-1] -a
        turn ++

    i = 2
    if turn


