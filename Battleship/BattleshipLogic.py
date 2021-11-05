from Battleship.Fleet import Fleet
import numpy as np


class GridMaker:
    LETTER_RANGE = 'abcdefghijklmnopqrstuvwxyz'.upper()

    def __init__(self, game_size, space_size=4):
        "Game size should be between 10-26"
        limited_value = min(game_size, 26)
        self.game_size = max(limited_value, 10)

        self.GRID_YOU = np.empty((10, 10), dtype=str)
        self.GRID_YOU[:] = "_"

        self.GRID_OPPONENT = np.empty((10, 10), dtype=str)
        self.GRID_OPPONENT[:] = "_"
        self.space_size = space_size

    def display_grids(self):
        grid_size = self.game_size + 1
        print(self.GRID_YOU.shape)
        for i in range(grid_size):
            for j in range(grid_size):
                if i == 0 and j == 0:
                    print(" " * (self.space_size + 1), end="")
                elif i == 0 and j != 0:
                    print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print(i, end=" " * (self.space_size - 1))
                    else:
                        print(i, end=" " * self.space_size)
                else:
                    print(self.GRID_YOU[i - 1, j - 1], end=" ")
            print(" " * 2 * self.space_size, end="")

            for j in range(grid_size):
                if i == 0 and j == 0:
                    print(" " * (self.space_size + 1), end="")
                elif i == 0 and j != 0:
                    print(self.LETTER_RANGE[j - 1], end=" ")
                elif i != 0 and j == 0:
                    if i >= 10:
                        print(i, end=" " * (self.space_size - 1))
                    else:
                        print(i, end=" " * self.space_size)
                else:
                    print(self.GRID_OPPONENT[i - 1, j - 1], end=" ")
            print("")

    def deploy_fleet(self):
        print("\n" * 3)
        print("---------------------DEPLOY YOUR FLEET--------------------")
        head, tail = self.get_locations(Fleet.CARRIER)
        print(head, tail)

    def get_locations(self, fleet_type):
        while True:
            print("DEPLOY YOUR {} (LENGTH {})".format(fleet_type.name, fleet_type.value))
            try:
                head = input("PLEASE SELECT THE LOCATION OF THE HEAD : ")
                tail = input("PLEASE SELECT THE LOCATION OF THE TAIL : ")

                "whitespaces will be ignored"
                head = head.strip()
                tail = tail.strip()

                if len(head) == 2 and len(tail) == 2 and (head[0] in self.LETTER_RANGE) and (
                        tail[0] in self.LETTER_RANGE) and (int(head[1]) in range(1, 11)) and (int(tail[1]) in range(1, 11)):

                    if head[0] == tail[0] or head[1] == tail[1]:
                        head_index_sum = GridMaker.LETTER_RANGE.index(head[0]) + int(head[1])
                        tail_index_sum = GridMaker.LETTER_RANGE.index(tail[0]) + int(tail[1])
                        len_ship = abs(head_index_sum - tail_index_sum) + 1

                        if len_ship == fleet_type.value:
                            head = int(head[1])-1, GridMaker.LETTER_RANGE.index(head[0])
                            tail = int(tail[1])-1, GridMaker.LETTER_RANGE.index(tail[0])
                            return head, tail

                        print("Length of the {} must be {}".format(fleet_type.name, fleet_type.value))
                        print("Please try again...")
                        continue

                    else:
                        print("Ship cannot be deployed diagonal!")
                        print("Please try again...")
                        continue

                else:
                    print("Mismatched location")
                    print("Please try again...")

            except Exception as e:
                print(e)
                print("Mismatched Input")
                print("Please try again...")
                continue


grid = GridMaker(game_size=10, space_size=4)
grid.display_grids()
grid.deploy_fleet()
