import socket
import sys

from playsound import playsound

from Battleship.Game import Game
import pickle
import numpy
from prompt_toolkit.shortcuts import prompt
import traceback
from prompt_toolkit.styles import Style
import os
from prompt_toolkit import print_formatted_text, HTML, ANSI
from  keyboard import press
from Battleship.ShipText import ShipText


os.system("mode con cols=140 lines=40")
#press("F11")


MESSAGE_TAKEN = None
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)




def open_client():
    global  ADDR
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.connect(ADDR)
    return client

def send(msg,client):
    global MESSAGE_TAKEN
    message = msg
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    recvd_data = client.recv(2048)
    MESSAGE_TAKEN = pickle.loads(recvd_data)
    client.close()

    #print("Message is taken.")

def send_and_wait(message_sent,client):
    global MESSAGE_TAKEN,ADDR
    content=None
    connected = False
    while not connected:
        try:
            client.connect(ADDR)
            connected = True
        except Exception as e:
            pass  # Do nothing, just try again

    while MESSAGE_TAKEN is None:
        try:
            send(msg=pickle.dumps(message_sent),client=client)
            content = MESSAGE_TAKEN
        except Exception as e:
            if e is None:
                print("problem is not found?!")
                continue
            print(e)
            print(traceback.format_exc())  # print stack trace
            break
    MESSAGE_TAKEN=None
    return content


def play():
    global MESSAGE_TAKEN
    Game.Welcome()

    style = Style.from_dict({
        # User input (default text).
        '': 'ansigreen ',

        # Prompt.
        'sentence': '#FFFFFF',
        'key': '#ff0066 underline',
        'column' : '#FFFFFF'

    })

    message = [
        ('class:sentence', "Pick a "),
        ('class:key', 'username'),
        ('class:column', ' :')
    ]
    username_client = prompt(message=message,style=style)
    if username_client.strip() == "": username_client = "YOU"
    username_server = ""


    print_formatted_text(HTML('<ansiyellow>\nWaiting for other player to pick a username!\n</ansiyellow>'))

    #0
    username_sent = username_client
    if username_sent=="YOU": username_sent="OPPONENT"
    client = open_client()
    username_server = send_and_wait(message_sent=username_sent,client=client)

    game = Game(username1=username_client,username2=username_server)
    game.start_game()

    print_formatted_text(HTML('<ansiyellow>\n\tWaiting for other player to deploy his/her fleet!\n</ansiyellow>'))
    winner=None

    while True:


        # ------------------------1-------------------------------
        print_formatted_text(HTML('<ansiyellow>\n\tWaiting for other player\'s move!\n</ansiyellow>'))
        client = open_client()
        grid_from_server = send_and_wait(message_sent=game.GRID_YOU,client=client)

        # ------------------------2-------------------------------
        client = open_client()
        msg ="WAITING"
        msg_recvd= send_and_wait(message_sent=msg,client=client)
        if isinstance(msg_recvd,str) and msg_recvd=="LOSE": #YOU LOST
            winner=game.username2.upper()

            game.clear_console()
            game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
            print_formatted_text(HTML('<ansired>\n\n{}</ansired>').format(ShipText.LOSE.value))
            playsound('D:\Dersler\____2021-2022\CS 447\HW1\Sound\lose.mp3')
            break
        game.GRID_YOU = msg_recvd

        # ------------------------3-------------------------------
        text = "\nYour turn "+game.username1.upper()+" !"
        print_formatted_text(HTML('<ansigreen>{}</ansigreen>').format(text))
        game.all_locs_opponent_r,grid_from_server = game.make_guess(username=username_client,
                                                                    opponent_grid_real=grid_from_server,
                                                                    opponent_grid_relative=game.GRID_OPPONENT_R,
                                                                    possible_locs_opponent_r=game.all_locs_opponent_r)
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU,grid_opponent_r=game.GRID_OPPONENT_R)
        if game.is_game_finished(grid_from_server): #YOU WIN
            winner=game.username1.upper()
            client = open_client()
            msg = "LOSE"
            send_and_wait(message_sent=msg,client=client)

            game.clear_console()
            game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
            print_formatted_text(HTML('<ansigreen>\n\n{}</ansigreen>').format(ShipText.WIN.value))
            playsound('D:\Dersler\____2021-2022\CS 447\HW1\Sound\\victory.mp3')
            break
        client = open_client()
        send_and_wait(message_sent=grid_from_server,client=client)



if __name__ == "__main__":
    sys.exit(play())
