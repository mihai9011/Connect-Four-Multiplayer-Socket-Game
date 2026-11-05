# Connect 4 - Client-Server TCP Game

A classic Connect 4 game implemented in a Client-Server architecture using the TCP protocol. The server supports multithreaded connections, allowing multiple pairs of players to play simultaneously.

## Technologies

* Server: Python 3 (socket, struct, threading)
* Client: C (POSIX sockets / adapted Winsock)
* Protocol: TCP

## How to run on Windows

You need Python 3 and a C compiler (such as MinGW or via WSL) installed on your system.

1. Compiling the client
   Open a terminal (Command Prompt, PowerShell, or WSL) in the project folder and compile the C code:
   ```bash
   gcc client.c -o client.exe
   ```

2. Starting the server
   Open the first terminal and run the server. It will start listening for new connections:
   ```bash
   python server.py
   ```

3. Connecting the clients
   Open two other completely separate terminals (for Player 1 and Player 2). In both, run the newly compiled client:
   ```bash
  ./client.exe
   ```
 
