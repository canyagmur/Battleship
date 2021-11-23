from Fleet import Fleet
import numpy as np
from prompt_toolkit import print_formatted_text, HTML,ANSI
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.completion import WordCompleter
import os


class GridMaker:
    LETTER_RANGE = 'abcdefghijklmnopqrstuvwxyz'.upper()  # ALPHABET
    PLACE_HOLDER = "-"

    def __init__(self, game_size, space_size=4):

        """Game size should be between 10-26"""
        limited_value = min(game_size, 26)
        self.game_size = max(limited_value, 10)

        self.GRID_YOU = np.empty((self.game_size, self.game_size), dtype=str)
        self.GRID_YOU[:] = self.PLACE_HOLDER

        self.GRID_OPPONENT = np.empty((self.game_size, self.game_size), dtype=str)
        self.GRID_OPPONENT[:] = self.PLACE_HOLDER
        self.space_size = space_size

        self.all_locations = []
        for letter in self.LETTER_RANGE[0:self.game_size]:
            for number in range(1,self.game_size+1):
                self.all_locations.append(letter+str(number))

    def display_grids(self):
        grid_size = self.game_size + 1
        for i in range(grid_size):
            for j in range(grid_size):
                if i == 0 and j == 0:
                    print_formatted_text(" " * (self.space_size + 1), end="")
                elif i == 0 and j != 0:
                    mytext = self.LETTER_RANGE[j - 1]
                    print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(mytext),end=" ") #print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(i), end=" " * (self.space_size - 1)) #print_formatted_text(i, end=" " * (self.space_size - 1))
                    else:
                        print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(i), end=" " * self.space_size)#print_formatted_text(i, end=" " * self.space_size)
                else:
                    mytext=self.GRID_YOU[i - 1, j - 1]
                    print_formatted_text(HTML('<b><ansigreen>{}</ansigreen></b>').format(mytext), end=" ")
            print_formatted_text(" " * 2 * self.space_size, end="")

            for j in range(grid_size):
                if i == 0 and j == 0:
                    #print(" " * (self.space_size + 1), end="")
                    mytext = " " * (self.space_size + 1)
                    print_formatted_text(mytext,end="")
                elif i == 0 and j != 0:
                    mytext = self.LETTER_RANGE[j - 1]
                    print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(mytext), end=" ")
                    #print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(i), end=" " * (self.space_size - 1)) #print_formatted_text(i, end=" " * (self.space_size - 1))
                    else:
                        print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(i), end=" " * self.space_size)#print_formatted_text(i, end=" " * self.space_size)
                else:
                    mytext=self.GRID_OPPONENT[i - 1, j - 1]
                    print_formatted_text(HTML('<b><ansigreen>{}</ansigreen></b>').format(mytext), end=" ")
                    #print(self.GRID_OPPONENT[i - 1, j - 1], end=" ")
            print_formatted_text("")  # NEW LINE
            if i == 0: print_formatted_text("")

    def deploy_fleet(self):
        print_formatted_text("\n" * 3)
        print_formatted_text(HTML('<ansiwhite><i>---------------------DEPLOY YOUR FLEET--------------------</i></ansiwhite>'))

        fleet_enums = [i for i in Fleet]

        possible_locs = self.all_locations.copy()

        for ship_enum in fleet_enums:
            head, tail = self.get_locations(ship_enum,possible_locs)
            while True:
                if self.is_block_empty(head, tail):
                    possible_locs=self.put_ship(head, tail, ship_enum,possible_locs)
                    break
                else:
                    print_formatted_text(HTML("<ansired>Overlapping blocks for ships detected!</ansired>"))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    head, tail = self.get_locations(ship_enum,possible_locs)
                    continue
        print_formatted_text("\n"*3)
        print_formatted_text(HTML('<ansicyan>The fleet is ready for your command!</ansicyan>'))

        self.display_grids()

    def is_grid_valid_and_empty(self,loc,available_locs):
        return loc in available_locs


    def is_block_empty(self, head, tail):
        x_h, y_h = head
        x_t, y_t = tail
        start_x, end_x = tuple(sorted([x_t, x_h]))
        start_y, end_y = tuple(sorted([y_t, y_h]))
        filter_list = self.GRID_YOU[start_x:end_x + 1, start_y:end_y + 1] == self.PLACE_HOLDER
        return False not in filter_list

    def put_ship(self, head, tail, fleet_type,possible_locs):
        text = "{} is deployed !".format(fleet_type.name)
        print_formatted_text(HTML("<ansigreen>{}</ansigreen>").format(text))
        x_h, y_h = head
        x_t, y_t = tail
        start_x, end_x = tuple(sorted([x_t, x_h]))
        start_y, end_y = tuple(sorted([y_t, y_h]))
        self.GRID_YOU[start_x:end_x + 1, start_y:end_y + 1] = fleet_type.name[0]
        for i in range(start_x,end_x+1):
            for j in range(start_y,end_y+1):
                loc = self.LETTER_RANGE[j]+str(i+1)
                possible_locs.remove(loc)
        return  possible_locs


    def get_locations(self, fleet_type,available_loc_list):
        while True:
            text = '                    _~      \n\
                _~ )_)_~   \n\
                )_))_))_)   DEPLOY YOUR {} (LENGTH {})\n\
                _!__!__!_   \n\
                \______t/  \n\
              ~~~~~~~~~~~~~'.format(fleet_type.name, fleet_type.value)
            #text ="DEPLOY YOUR {} (LENGTH {})".format(fleet_type.name, fleet_type.value)
            print_formatted_text(HTML("<ansigreen>{}</ansigreen>").format(text))
            try:

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
                    ('class:username', 'can'),
                    ('class:at', '@'),
                    ('class:host', 'localhost'),
                    ('class:colon', ':'),
                    ('class:pound', '# '),
                ]


                loc_completer = WordCompleter(available_loc_list)  # autocompleter

                print_formatted_text(HTML('<ansiyellow>\tPLEASE SELECT THE LOCATION OF THE HEAD : </ansiyellow>'))
                head = prompt(message, style=style,completer=loc_completer)

                other_locs =[]
                if self.is_grid_valid_and_empty(head,available_loc_list):
                    letter = head[0]
                    number = int(head[1:])
                    ship_size = fleet_type.value

                    letter_1 = chr(ord(letter)-ship_size+1) #search below
                    letter_2 = chr(ord(letter)+ship_size-1) #search above

                    if ord(letter_1) >= ord("A") and self.is_grid_valid_and_empty((letter_1+str(number)),available_loc_list):
                        other_locs.append(letter_1+str(number))
                    if ord(letter_2) <= ord(self.LETTER_RANGE[self.game_size-1]) and self.is_grid_valid_and_empty((letter_2+str(number)),available_loc_list):
                        other_locs.append(letter_2+str(number))

                    number_1 = number-ship_size+1 #search below
                    number_2 = number+ship_size-1 #search above

                    if number_1 >= 1 and self.is_grid_valid_and_empty((letter+str(number_1)),available_loc_list)  :
                        other_locs.append(letter+str(number_1))

                    if number_2 <= self.game_size and self.is_grid_valid_and_empty((letter+str(number_2)),available_loc_list):
                        other_locs.append(letter+str(number_2))

                    #other_locs = [x for x in available_loc_list.copy() if x.startswith(head[0]) or x.endswith(head[1:])]
                else:
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue

                loc_completer = WordCompleter(other_locs)

                print_formatted_text(HTML('<ansiyellow>\tPLEASE SELECT THE LOCATION OF THE TAIL : </ansiyellow>'))
                tail = prompt(message, style=style,completer=loc_completer)

                if tail in available_loc_list:
                    head = head.strip()
                    tail = tail.strip()
                else:
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue
                "whitespaces will be ignored"


                if (head in available_loc_list) and (tail in available_loc_list):

                    if head[0] == tail[0] or head[1:] == tail[1:]:
                        head_index_sum = GridMaker.LETTER_RANGE.index(head[0]) + int(head[1:])
                        tail_index_sum = GridMaker.LETTER_RANGE.index(tail[0]) + int(tail[1:])
                        len_ship = abs(head_index_sum - tail_index_sum) + 1

                        if len_ship == fleet_type.value:
                            head = int(head[1:]) - 1, GridMaker.LETTER_RANGE.index(head[0])
                            tail = int(tail[1:]) - 1, GridMaker.LETTER_RANGE.index(tail[0])

                            return head, tail

                        text ="\nLength of the {} must be {}".format(fleet_type.name, fleet_type.value)
                        print_formatted_text(HTML('<ansired>{}</ansired>'.format(text)))
                        print_formatted_text(HTML('<ansired>\nPlease try again...</ansired>'))
                        continue

                    else:
                        print_formatted_text(HTML('<ansired>Ship cannot be deployed diagonal!</ansired>'))
                        print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                        continue

                else: #unnecessary
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))

            except Exception as e:
                print_formatted_text(e)
                print_formatted_text(HTML('<ansired>Input format is wrong!</ansired>'))
                print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                continue




def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)




clearConsole()

grid = GridMaker(game_size=20, space_size=4)
grid.display_grids()
grid.deploy_fleet()
