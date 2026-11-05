from connectFour import ConnectFourGame
import socket

# matchmacking
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(("0.0.0.0", 5555))
s.listen(10) # up to 10 connections

print("Server Matchmaking open! Waiting for players...")

waiting_player = None

while True:
    
    client, addr = s.accept()
    print(f"PLayer connected at {addr}")
    
    if waiting_player is None:
        # first client waits
        waiting_player = client
        print("Waiting for second player to start game...")
    else:
        # we have a pair, start a thread
        game_thread = ConnectFourGame(waiting_player, client)

        #calls automatically the overriden run() function from extended Thread class
        game_thread.start()
        
        # reset it for the next pair
        waiting_player = None
