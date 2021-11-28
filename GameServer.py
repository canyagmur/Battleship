import argparse
import socket
import threading
from Battleship.Game import Game
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit import print_formatted_text, HTML, ANSI
import pickle
import sys
import os
from playsound import playsound
from Battleship.ShipText import ShipText

os.system("mode con cols=140 lines=40")

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


def open_server():
    global ADDR

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    return server


def handle_client(conn, addr, server_message):
    # print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER)
        if msg_length:
            msg_length = int(msg_length)
            recvd_data = conn.recv(msg_length)
            recvd_data = pickle.loads(recvd_data)

            # print(f"[{addr}] {MESSAGE}")
            # print("Message is taken!")
            conn.send(pickle.dumps(server_message))
            break

    conn.close()
    return  recvd_data


def connect(message_sent, server):
    server.listen()
    recvd_data = None
    while recvd_data is None:
        conn, addr = server.accept()
        recvd_data=handle_client(conn, addr, message_sent)
        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    server.close()
    return recvd_data


def play():
    Game.Welcome()  # hi to server

    style = Style.from_dict({
        # User input (default text).
        '': 'ansigreen ',

        # Prompt.
        'sentence': '#FFFFFF',
        'key': '#ff0066 underline',
        'column': '#FFFFFF'

    })

    message = [
        ('class:sentence', "Pick a "),
        ('class:key', 'username'),
        ('class:column', ' :')
    ]

    # Ask server to pick a username (here) //username_server
    username_server = prompt(message=message, style=style)
    if username_server.strip() == "": username_server = "YOU"

    print_formatted_text(HTML('<ansiyellow>\nWaiting for other player to pick a username!\n</ansiyellow>'))

    # Ask client to pick a username and send server's username back to client. // username_client
    username_sent = username_server
    if username_sent == "YOU": username_sent = "OPPONENT"
    server = open_server()
    username_client =connect(message_sent=username_sent, server=server)


    game = Game(username1=username_server, username2=username_client)
    game.start_game()

    # print("\nGame is starting .....") # I WILL RETURN HERE
    print_formatted_text(HTML('<ansiyellow>\n\tWaiting for other player to deploy his/her fleet!\n</ansiyellow>'))
    winner = None

    while True:

        # Ask client to give its GRID and send server's back.//////grid_from_client

        # ------------------------1-------------------------------
        #Player 1 makes guess
        server = open_server()
        grid_from_client=connect(message_sent=game.GRID_YOU, server=server)


        text = "\nYour turn " + game.username1.upper() + " !"
        print_formatted_text(HTML('<ansigreen>{}</ansigreen>').format(text))

        game.all_locs_opponent_r, grid_from_client = game.make_guess(username=username_server,
                                                                     opponent_grid_real=grid_from_client,
                                                                     opponent_grid_relative=game.GRID_OPPONENT_R,
                                                                     possible_locs_opponent_r=game.all_locs_opponent_r)
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)

        if game.is_game_finished(grid_from_client):  # YOU WIN
            winner = game.username1.upper()
            server = open_server()
            connect(message_sent="LOSE", server=server)

            game.clear_console()
            game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
            print_formatted_text(HTML('<ansigreen>\n\n{}</ansigreen>').format(ShipText.WIN.value))
            playsound('.\Sound\\victory.mp3')
            break

        # ------------------------2-------------------------------
        # Send client grid_ back to client. #WAITING
        server = open_server()
        connect(message_sent=grid_from_client, server=server)

        # ------------------------3-------------------------------
        # now its client's turn... wait for its move and your updated grid.
        print_formatted_text(HTML('<ansiyellow>\n\tWaiting for other player\'s move!\n</ansiyellow>'))
        server = open_server()
        message_taken = connect(message_sent="WAITING", server=server)
        if isinstance(message_taken, str) and message_taken == "LOSE":  # YOU LOST
            winner = game.username2.upper()

            game.clear_console()
            game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
            print_formatted_text(HTML('<ansired>\n\n{}</ansired>').format(ShipText.LOSE.value))
            playsound('.\Sound\lose.mp3')
            break

        game.GRID_YOU = message_taken


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Process PORT number')
    # parser.add_argument('-p', '--port', help='specify a port number', required=False,default=5050,type=int)
    # args = vars(parser.parse_args())
    #
    # PORT = args['port']
    # ADDR = (SERVER,PORT)

    sys.exit(play())
