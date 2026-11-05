import socket
import struct
import threading

#class becomes a thread, so match between 2 players
class ConnectFourGame(threading.Thread):
    def __init__(self, player1_socket, player2_socket):
        super().__init__() 
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.players = [player1_socket, player2_socket]
    
    def run(self):
        print(f"New game between {self.players[0].getpeername()} and {self.players[1].getpeername()}")
        self.game_loop()
        
        # closing connections
        self.players[0].close()
        self.players[1].close()

    # id_gamestate : 1 - can choose column,3 - wait,  2 - won game , 0 - lost game , -1 - column full
    def send_gamestate(self, client_socket,  id_gamestate):
        board_str = "".join(str(cell) for row in self.board for cell in row)

        board_bytes = board_str.encode('ascii')

        #baord has 64 bytes, with the endline 65
        packet = struct.pack("@65si", board_bytes,id_gamestate)

        client_socket.sendall(packet)

    def find_level(self, col:int):
        column = []

        for i in range(8):
            column.append(self.board[i][col])

        if column[7] != 0:
                return -1

        i = len(column) - 1;

        while(column[i] == 0 and i > 0):
            i = i - 1
        
        if(i == 0 and column[0] != 0):return 1
        elif(i == 0 and column[0] == 0):return 0

        return i + 1

    def game_loop(self):
        ok = True
        player_turn = 0

        while ok:
            self.send_gamestate(self.players[player_turn % 2], 1)
            self.send_gamestate(self.players[(player_turn + 1) % 2], 3) 

            current_socket = self.players[player_turn % 2]
            
            try:
                col = current_socket.recv(4)
                if not col: break # In case a client disconnects
            except:
                break
            
            column = struct.unpack("i", col)[0]
            changed = False
            if column > 7 or column < 0: continue

            level = self.find_level(column)

            while level == -1:
                self.send_gamestate(self.players[player_turn % 2], -1)
                
                try:
                    col = current_socket.recv(4)
                    if not col: break
                except:
                    break
                    
                column = struct.unpack("i", col)[0]
                level = self.find_level(column)
             
            self.board[level][column] = player_turn % 2 + 1
            changed = True

            if changed and self.four_connected(level, column, player_turn % 2 + 1):
                ok = False
                self.send_gamestate(self.players[player_turn % 2], 2)
                self.send_gamestate(self.players[(player_turn + 1) % 2], 0)
                
            player_turn += 1

    def display_board(self):
        for i in range(7,-1,-1):
            print(self.board[i])
            print()
    
    def four_connected(self, row: int, col: int, numb: int) -> bool:

        if self.board[row][col] != numb:
            return False

        #directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for d_row, d_col in directions:
            count = 1  
            
            r = row + d_row
            c = col + d_col
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == numb:
                count += 1
                r += d_row
                c += d_col

            r = row - d_row
            c = col - d_col
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == numb:
                count += 1
                r -= d_row
                c -= d_col

            if count >= 4:
                return True

        return False

