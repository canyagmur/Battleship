from Battleship.BattleshipLogic import GridMaker
from Battleship.ShipText import ShipText
import os
import time
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text, HTML, ANSI
import numpy as np
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import prompt
import traceback
import sys
from playsound import playsound






class Game():
    PLACE_HOLDER = "-"
    GRID_YOU = None
    GRID_OPPONENT = None

    GRID_FLEET_NAMES = ['C','B','S','D']

    def __init__(self, username1="User-1", username2="User-2", game_size=10, space_size=4):
        """Usernames"""
        self.username1 = username1
        self.username2 = username2

        """Game size should be between 10-26"""
        limited_value = min(game_size, 26)
        self.game_size = max(limited_value, 10)
        self.space_size = space_size

        self.GRID_YOU = np.empty((self.game_size, self.game_size), dtype=str)
        self.GRID_YOU[:] = self.PLACE_HOLDER

        self.GRID_OPPONENT_R = np.empty((self.game_size, self.game_size), dtype=str)
        self.GRID_OPPONENT_R[:] = self.PLACE_HOLDER

        """Grid Maker Object"""
        self.grid_maker = GridMaker(game_size=self.game_size, space_size=self.space_size, username1=username1,
                                    username2=username2, PLACE_HOLDER=self.PLACE_HOLDER)

        self.all_locs_opponent_r = self.grid_maker.all_locations.copy()


        self.HIT_SYMBOL = self.grid_maker.HIT_SYMBOL
        self.MISS_SYMBOL = self.grid_maker.MISS_SYMBOL

    def DISPLAY_GRIDS(self,grid_you, grid_opponent_r):
        self.grid_maker.display_grids(grid_you=grid_you,grid_opponent_r=grid_opponent_r)

    @classmethod
    def clear_console(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    @classmethod
    def Welcome(self):
        """CLEAN CONSOLE AND WELCOME SCREEN"""
        self.clear_console()
        print_formatted_text(HTML("<ansiwhite>{}</ansiwhite>").format(ShipText.WELCOME.value))
        playsound(r".\Sound\Aoe2-vikings2.mp3") #downgrade to playsound1.2.2!
        print("\n" * 3)


    def start_game(self):

        self.grid_maker.display_grids(self.GRID_YOU, self.GRID_OPPONENT_R)
        self.GRID_YOU = self.grid_maker.deploy_fleet(username=self.username1, GRID_YOU=self.GRID_YOU,
                                                     GRID_OPPONENT_R=self.GRID_OPPONENT_R)



    def is_game_finished(self,grid):
        has_true = False
        for char in self.GRID_FLEET_NAMES:
            has_true = has_true or (char in grid)
        return not has_true # if it has no characters then game is finished.

    def convert_coordinate(self,location):
        coor = int(location[1:]) - 1, GridMaker.LETTER_RANGE.index(location[0])

        return coor

    def make_guess(self,opponent_grid_real,opponent_grid_relative,username,possible_locs_opponent_r):
        style = Style.from_dict({
            # User input (default text).
            '': '#ff0066',

            # Prompt.
            'username': 'ansicyan underline',
            'at': '#00aa00',
            'colon': '#0000aa',
            'pound': '#00aa00',
            'host': '#00ffff ',
        })

        message = [
            ('class:username', username),
            ('class:at', '@'),
            ('class:host', 'localhost'),
            ('class:colon', ':'),
            ('class:pound', '# '),
        ]
        loc_completer = WordCompleter(possible_locs_opponent_r)

        loc_copy = possible_locs_opponent_r.copy()

        while True:
            try:
                print_formatted_text(HTML('<ansiyellow>\n\tPLEASE MAKE A GUESS\n</ansiyellow>'))
                guess = prompt(message, style=style, completer=loc_completer)
                if guess in self.grid_maker.all_locations :   #It checks whether the guess is wrong formatted or not.
                     if guess in loc_copy:
                        """From now on guess is valid"""
                        x,y = self.convert_coordinate(guess)
                        value = opponent_grid_real[x,y]
                        loc_copy.remove(guess)
                        if value in self.GRID_FLEET_NAMES: #hit condition
                            playsound(".\Sound\ship-sunk-aoe2.mp3")
                            opponent_grid_real[x,y] = self.HIT_SYMBOL
                            opponent_grid_relative[x,y] = self.HIT_SYMBOL
                            return  loc_copy,opponent_grid_real
                        else:
                            playsound(".\Sound\miss.mp3")
                            opponent_grid_real[x,y] = self.MISS_SYMBOL
                            opponent_grid_relative[x,y] = self.MISS_SYMBOL
                            return loc_copy,opponent_grid_real

                     else:
                        print_formatted_text(HTML('<ansired>This place already marked</ansired>'))
                        print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                        continue
                else:
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue

            except Exception as e:
                if e is None:
                    print_formatted_text(HTML('<ansired>Input format is wrong!</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue
                #print_formatted_text(e)
                #print_formatted_text(traceback.format_exc())  # print stack trace
                break


# game = Game(game_size=10)
# game.start_game()
