from Battleship.Fleet import Fleet
import numpy as np
from prompt_toolkit import print_formatted_text, HTML, ANSI
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.completion import WordCompleter
import os
from Battleship.ShipText import ShipText
import traceback
from playsound import playsound


class GridMaker:
    LETTER_RANGE = 'abcdefghijklmnopqrstuvwxyz'.upper()  # ALPHABET
    all_locations = []
    BUILD_SOUND_PATHS = ['.\Sound\yaparım1.mp3',
                         '.\Sound\yaparım2.mp3',
                         '.\Sound\yaparım3.mp3',
                         '.\Sound\yaparım4.mp3'
                         ]

    HIT_SYMBOL = "H"
    MISS_SYMBOL ="X"

    def __init__(self, game_size, username1, username2, space_size, PLACE_HOLDER):
        self.game_size = game_size
        self.space_size = space_size
        self.username1 = username1
        self.username2 = username2
        self.PLACE_HOLDER = PLACE_HOLDER

        for letter in self.LETTER_RANGE[0:self.game_size]:
            for number in range(1, self.game_size + 1):
                self.all_locations.append(letter + str(number))

    def display_grids(self, grid_you, grid_opponent_r):
        grid_size = self.game_size + 1

        text = " " * (self.space_size + self.game_size - 1) + self.username1.upper()
        print_formatted_text(HTML("<ansicyan>{}</ansicyan>").format(text), end="")
        print_formatted_text(" " * 2 * self.space_size, end="")
        text = " " * (self.space_size + 2 * self.game_size - 2) + self.username2.upper()
        print_formatted_text(HTML("<ansicyan>{}</ansicyan>").format(text), end="\n\n")

        for i in range(grid_size):
            for j in range(grid_size):
                if i == 0 and j == 0:
                    print_formatted_text(" " * (self.space_size + 1), end="")
                elif i == 0 and j != 0:
                    mytext = self.LETTER_RANGE[j - 1]
                    print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(mytext),
                                         end=" ")  # print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(i), end=" " * (
                                self.space_size - 1))  # print_formatted_text(i, end=" " * (self.space_size - 1))
                    else:
                        print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(i),
                                             end=" " * self.space_size)  # print_formatted_text(i, end=" " * self.space_size)
                else:
                    mytext = grid_you[i - 1, j - 1]
                    if mytext == self.HIT_SYMBOL : print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(mytext), end=" ")
                    elif mytext == self.MISS_SYMBOL : print_formatted_text(HTML('<b><ansigreen>{}</ansigreen></b>').format(mytext), end=" ")
                    else: print_formatted_text(HTML('<b><ansiwhite>{}</ansiwhite></b>').format(mytext), end=" ")

            print_formatted_text(" " * 2 * self.space_size, end="")
            for j in range(grid_size):
                if i == 0 and j == 0:
                    # print(" " * (self.space_size + 1), end="")
                    mytext = " " * (self.space_size + 1)
                    print_formatted_text(mytext, end="")
                elif i == 0 and j != 0:
                    mytext = self.LETTER_RANGE[j - 1]
                    print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(mytext), end=" ")
                    # print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(i), end=" " * (
                                self.space_size - 1))  # print_formatted_text(i, end=" " * (self.space_size - 1))
                    else:
                        print_formatted_text(HTML('<b><ansiyellow>{}</ansiyellow></b>').format(i),
                                             end=" " * self.space_size)  # print_formatted_text(i, end=" " * self.space_size)
                else:
                    mytext = grid_opponent_r[i - 1, j - 1]
                    if mytext == self.HIT_SYMBOL : print_formatted_text(HTML('<b><ansigreen>{}</ansigreen></b>').format(mytext), end=" ")
                    elif mytext == self.MISS_SYMBOL : print_formatted_text(HTML('<b><ansired>{}</ansired></b>').format(mytext), end=" ")
                    else: print_formatted_text(HTML('<b><ansiwhite>{}</ansiwhite></b>').format(mytext), end=" ")

                    # print(self.GRID_OPPONENT[i - 1, j - 1], end=" ")
            print_formatted_text("")  # NEW LINE
            if i == 0: print_formatted_text("")

    def deploy_fleet(self, username, GRID_YOU, GRID_OPPONENT_R):

        print_formatted_text("\n" * 3)
        print_formatted_text(
            HTML('<ansiwhite><i>---------------------DEPLOY YOUR FLEET--------------------</i></ansiwhite>'))
        print_formatted_text("\n" * 2)
        fleet_enums = [i for i in Fleet]

        possible_locs = self.all_locations.copy()

        for ship_enum in fleet_enums:
            head, tail = self.get_locations(ship_enum, possible_locs, username)
            while True:
                if self.is_block_empty(head, tail, GRID_YOU):
                    possible_locs = self.put_ship(head, tail, ship_enum, possible_locs, GRID_YOU)
                    break
                else:
                    print_formatted_text(HTML("<ansired>Overlapping blocks for ships detected!</ansired>"))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    head, tail = self.get_locations(ship_enum, possible_locs, username)
                    continue
        print_formatted_text("\n" * 3)
        print_formatted_text(HTML('<ansigreen>\t\tThe fleet is ready for your command!\n\n</ansigreen>'))

        self.display_grids(GRID_YOU, GRID_OPPONENT_R)
        return GRID_YOU

    def is_grid_valid_and_empty(self, loc, available_locs):
        return loc in available_locs

    def is_block_empty(self, head, tail, USER):
        x_h, y_h = head
        x_t, y_t = tail
        start_x, end_x = tuple(sorted([x_t, x_h]))
        start_y, end_y = tuple(sorted([y_t, y_h]))
        filter_list = USER[start_x:end_x + 1, start_y:end_y + 1] == self.PLACE_HOLDER
        return False not in filter_list

    def put_ship(self, head, tail, fleet_type, possible_locs, USER):
        playsound(self.BUILD_SOUND_PATHS[fleet_type.value-2])
        print_formatted_text("\n" * 2)
        text = "\t\t\t{} is deployed !".format(fleet_type.name)
        print_formatted_text(HTML("<ansicyan>{}</ansicyan>").format(text))
        print_formatted_text("\n" * 2)
        x_h, y_h = head
        x_t, y_t = tail
        start_x, end_x = tuple(sorted([x_t, x_h]))
        start_y, end_y = tuple(sorted([y_t, y_h]))
        USER[start_x:end_x + 1, start_y:end_y + 1] = fleet_type.name[0]
        for i in range(start_x, end_x + 1):
            for j in range(start_y, end_y + 1):
                loc = self.LETTER_RANGE[j] + str(i + 1)
                possible_locs.remove(loc)
        return possible_locs

    def get_locations(self, fleet_type, available_loc_list, username):
        while True:
            if fleet_type.name == "CARRIER": text = ShipText.CARRIER.value
            if fleet_type.name == "BATTLESHIP": text = ShipText.BATTLESHIP.value
            if fleet_type.name == "SUBMARINE": text = ShipText.SUBMARINE.value
            if fleet_type.name == "DESTROYER": text = ShipText.DESTROYER.value

            # text ="DEPLOY YOUR {} (LENGTH {})".format(fleet_type.name, fleet_type.value)
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
                    ('class:username', username),
                    ('class:at', '@'),
                    ('class:host', 'localhost'),
                    ('class:colon', ':'),
                    ('class:pound', '# '),
                ]

                loc_completer = WordCompleter(available_loc_list)  # autocompleter

                print_formatted_text(HTML('<ansiyellow>\tPLEASE SELECT THE LOCATION OF THE HEAD : </ansiyellow>'))
                head = prompt(message, style=style, completer=loc_completer)

                other_locs = []
                if self.is_grid_valid_and_empty(head, available_loc_list):
                    letter = head[0]
                    number = int(head[1:])
                    ship_size = fleet_type.value

                    letter_1 = chr(ord(letter) - ship_size + 1)  # search below
                    letter_2 = chr(ord(letter) + ship_size - 1)  # search above

                    if ord(letter_1) >= ord("A") and self.is_grid_valid_and_empty((letter_1 + str(number)),
                                                                                  available_loc_list):
                        other_locs.append(letter_1 + str(number))
                    if ord(letter_2) <= ord(self.LETTER_RANGE[self.game_size - 1]) and self.is_grid_valid_and_empty(
                            (letter_2 + str(number)), available_loc_list):
                        other_locs.append(letter_2 + str(number))

                    number_1 = number - ship_size + 1  # search below
                    number_2 = number + ship_size - 1  # search above

                    if number_1 >= 1 and self.is_grid_valid_and_empty((letter + str(number_1)), available_loc_list):
                        other_locs.append(letter + str(number_1))

                    if number_2 <= self.game_size and self.is_grid_valid_and_empty((letter + str(number_2)),
                                                                                   available_loc_list):
                        other_locs.append(letter + str(number_2))

                    # other_locs = [x for x in available_loc_list.copy() if x.startswith(head[0]) or x.endswith(head[1:])]
                else:
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue

                loc_completer = WordCompleter(other_locs)

                print_formatted_text(HTML('<ansiyellow>\tPLEASE SELECT THE LOCATION OF THE TAIL : </ansiyellow>'))
                tail = prompt(message, style=style, completer=loc_completer)

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

                        text = "\nLength of the {} must be {}".format(fleet_type.name, fleet_type.value)
                        print_formatted_text(HTML('<ansired>{}</ansired>'.format(text)))
                        print_formatted_text(HTML('<ansired>\nPlease try again...</ansired>'))
                        continue

                    else:
                        print_formatted_text(HTML('<ansired>Ship cannot be deployed diagonal!</ansired>'))
                        print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                        continue

                else:  # unnecessary
                    print_formatted_text(HTML('<ansired>Mismatched location</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))

            except Exception as e:
                if e is None:
                    print_formatted_text(HTML('<ansired>Input format is wrong!</ansired>'))
                    print_formatted_text(HTML('<ansired>Please try again...</ansired>'))
                    continue
                #print_formatted_text(e)
                #print(traceback.format_exc())  # print stack trace
                break
