#include <netinet/ip.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdio.h>


int sfd;
struct sockaddr_in soc;


struct Packet {
    char board[65];
    int id_gamestate; // 1 - can choose column, 2 - won game , 0 - lost game , -1 - other error
};

void print_board(const char board[65]){
        int matrix[8][8];

        for (int i = 0; i < 8; i++) {
                for (int j = 0; j < 8; j++) {
                        matrix[i][j] = board[i * 8 + j] - '0';
                }
        }
        for (int i = 7; i >= 0; i--) {
                for (int j = 0; j < 8; j++) {
                        printf("%d ", matrix[i][j]);
                }
                printf("\n");
        }
}

int main() {

  //making the connection
  sfd = socket(AF_INET, SOCK_STREAM, 0);

  soc.sin_family = AF_INET;
  soc.sin_port = htons(5555);
  soc.sin_addr.s_addr = inet_addr("127.0.0.1");

  //directly connecting
  connect(sfd, (struct sockaddr *)&soc, sizeof(soc));

  while(1){
      int col;
      struct Packet packet;

          //cleaning the struct, replacing all its residual bytes with 0
          memset(&packet, 0, sizeof(packet));

          int nr_bytes = recv(sfd, &packet, sizeof(packet), 0);

      if(nr_bytes == sizeof(packet)){
                        print_board(packet.board);

                        if(packet.id_gamestate == 3){
                                printf("Other player is making a move...\n");
                        }

                        if(packet.id_gamestate == 0){
                                printf("You lost the game!");
                                break;
                        }
                        if(packet.id_gamestate == 2){
                                printf("You won the game!");
                                break;
                        }
                        if(packet.id_gamestate == 1){

                            printf("Nr column:");
                            scanf("%d", &col);
                            col = col -1;

                            send(sfd, &col, sizeof(int), 0);
                                continue;
                        }
                        if(packet.id_gamestate == -1){
                                printf("Internal server error.");
                                break;
                        }
                        }
  }

  return 0;
}
