import socket
import sys
from Battleship.Game import Game
import pickle
import numpy
from prompt_toolkit.shortcuts import prompt
import traceback
from prompt_toolkit.styles import Style
import os


# os.system("mode con cols=300 lines=300") make fullscreen


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

def send_and_wait(msg,client):
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
            send(msg=pickle.dumps(msg),client=client)
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
    Game.clear_console()
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
    username_server = ""

    #0
    client = open_client()
    msg= username_client
    username_server=send_and_wait(msg=msg,client=client)

    game = Game(username1=username_client,username2=username_server)
    game.start_game()

    print("\nGame is starting .....")
    winner=None

    while True:
        game.clear_console()
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
        print("Waiting for other player's move!")
        #1
        client=open_client()
        msg = game.GRID_YOU
        grid_from_server = send_and_wait(msg=msg,client=client)

        #2
        client = open_client()
        msg ="WAITING"
        msg_recvd= send_and_wait(msg=msg,client=client)
        if isinstance(msg_recvd,str) and msg_recvd=="LOSE":
            winner=game.username2.upper()
            print(winner)
            break
        game.GRID_YOU = msg_recvd

        #3
        print("Your turn user2:")
        game.all_locs_opponent_r,grid_from_server = game.make_guess(username=username_client,opponent_grid_real=grid_from_server,opponent_grid_relative=game.GRID_OPPONENT_R,possible_locs_opponent_r=game.all_locs_opponent_r)
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU,grid_opponent_r=game.GRID_OPPONENT_R)
        if game.is_game_finished(grid_from_server):
            winner=game.username1.upper()
            client = open_client()
            msg = "LOSE"
            send_and_wait(msg=msg,client=client)
            break
        client = open_client()
        msg = game.GRID_YOU
        send_and_wait(msg=msg,client=client)

    print(winner)


play()


# MESSAGE_SENT = [3,2,1]
# send(pickle.dumps(MESSAGE_SENT))
# #send(DISCONNECT_MESSAGE)
# print(MESSAGE_TAKEN)