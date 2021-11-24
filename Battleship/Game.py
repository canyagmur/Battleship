from BattleshipLogic import GridMaker
from ShipText import ShipText
import os
import time


class Game():

    def __init__(self,username1="User-1",username2="User-2"):
        self.username1= username1
        self.username2 = username2
        self.grid_maker = GridMaker(game_size=20, space_size=4,username1=username1,username2=username2)


    def clear_console(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    def start_game(self):
        self.clear_console()
        print(ShipText.WELCOME.value)
        time.sleep(3)
        print("\n"*3)


        self.grid_maker.display_grids()
        self.grid_maker.deploy_fleet(user=1)
        self.grid_maker.deploy_fleet(user=2)



game = Game()
game.start_game()



