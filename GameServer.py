import socket
import threading
from  Battleship.Game import Game
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit import print_formatted_text, HTML, ANSI
import pickle



HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MESSAGE_TAKEN = None


def open_server():
    global  ADDR
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    return server






def handle_client(conn, addr,server_message):
    global MESSAGE_TAKEN
    #print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER)
        if msg_length:
            msg_length = int(msg_length)
            recvd_data = conn.recv(msg_length)
            MESSAGE_TAKEN = pickle.loads(recvd_data)

            #print(f"[{addr}] {MESSAGE}")
            #print("Message is taken!")
            conn.send(pickle.dumps(server_message))
            break

    conn.close()


def connect(message_sent,server):
    global MESSAGE_TAKEN
    server.listen()
    #print(f"[LISTENING] Server is listening on {SERVER}")
    while MESSAGE_TAKEN is None:
        conn, addr = server.accept()
        handle_client(conn, addr,message_sent)
        #print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    server.close()

def play():
    global MESSAGE_TAKEN
    Game.clear_console()
    Game.Welcome() #hi to server


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

    #Ask server to pick a username (here) //username_server
    username_server = prompt(message=message,style=style)




    #Ask client to pick a username and send server's username back to client. // username_client
    server = open_server()
    connect(message_sent=username_server,server=server)
    username_client = MESSAGE_TAKEN
    MESSAGE_TAKEN=None


    game = Game(username1=username_server,username2=username_client)
    game.start_game()


    print("\nGame is starting .....") # I WILL RETURN HERE
    winner=None
    while True:
        game.clear_console()
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU, grid_opponent_r=game.GRID_OPPONENT_R)
        #Ask client to give its GRID and send server's back.//////grid_from_client
        server = open_server()
        connect(message_sent=game.GRID_YOU,server=server)
        grid_from_client = MESSAGE_TAKEN
        MESSAGE_TAKEN=None
        print("Your turn user1:")

        game.all_locs_opponent_r,grid_from_client = game.make_guess(username=username_server,opponent_grid_real=grid_from_client,opponent_grid_relative=game.GRID_OPPONENT_R,possible_locs_opponent_r=game.all_locs_opponent_r)
        game.DISPLAY_GRIDS(grid_you=game.GRID_YOU,grid_opponent_r=game.GRID_OPPONENT_R)
        if game.is_game_finished(grid_from_client):
            winner=game.username1.upper()
            server = open_server()
            connect(message_sent="LOSE", server=server)
            print(winner)
            break
        # Send client grid_ back to client. #WAITING
        server = open_server()
        connect(message_sent=grid_from_client,server=server)
        MESSAGE_TAKEN=None

        #now its client's turn... wait for its move and your updated grid.
        print("Waiting for other player's move!")
        server = open_server()
        connect(message_sent="WAITING",server=server)
        if isinstance(MESSAGE_TAKEN,str) and MESSAGE_TAKEN=="LOSE":
            winner=game.username2.upper()
            print(winner)
            break

        game.GRID_YOU = MESSAGE_TAKEN
        MESSAGE_TAKEN = None



play()

# print("[STARTING] Server is starting...")
# connect(message_sent=[1,2,3])
# print(MESSAGE_TAKEN)
#MESSAGE_TAKEN=None #update to None state