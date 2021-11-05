from Battleship.Fleet import Fleet
import numpy as np
class GridMaker:
    LETTER_RANGE = 'abcdefghijklmnopqrstuvwxyz'.upper()
    def __init__(self,game_size,space_size=4):
        "Game size should be between 10-26"
        limited_value= min(game_size,26)
        self.game_size = max(limited_value,10)

        self.GRID_YOU = np.zeros((self.game_size,self.game_size),dtype=int)
        self.GRID_OPPONENT = np.ones((self.game_size,self.game_size),dtype=int)
        self.space_size = space_size

    def displayGrids(self):
        grid_size =self.game_size+1
        print(self.GRID_YOU.shape)
        for i in range(grid_size):
            for j in range(grid_size):
                if i==0 and j == 0:
                    print(" "*(self.space_size+1),end="")
                elif i==0 and j!=0:
                    print(self.LETTER_RANGE[j-1],end=" ")
                elif i!=0 and j==0:
                    if i>=10 : print(i,end=" "*(self.space_size-1))
                    else: print(i,end=" "*self.space_size)
                else:
                    print(self.GRID_YOU[i-1,j-1],end=" ")
            print(" "*2*self.space_size,end="")

            for j in range(grid_size):
                if i==0 and j == 0:
                    print(" "*(self.space_size+1),end="")
                elif i==0 and j!=0:
                    print(self.LETTER_RANGE[j-1],end=" ")
                elif i!=0 and j==0:
                    if i>=10 : print(i,end=" "*(self.space_size-1))
                    else: print(i,end=" "*self.space_size)
                else:
                    print(self.GRID_OPPONENT[i-1,j-1],end=" ")
            print("")



grid = GridMaker(game_size=10,space_size=4)
grid.displayGrids()