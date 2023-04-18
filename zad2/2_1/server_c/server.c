#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(void)
{
    int socket_desc, client_sock, client_size, rval;
    struct sockaddr_in server_addr, client_addr;
    char server_message[2000], client_message[2000];
    
    // Prepare response buffer:
    memset(server_message, '\0', sizeof(server_message));
    strcpy(server_message, "This is the server's message.");
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if(socket_desc < 0){
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");
    
    // Set port and IP:
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(2000);
    
    // Bind to the set port and IP:
    if(bind(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr))<0){
        printf("Couldn't bind to the port\n");
        return -1;
    }
    printf("Done with binding\n");
    
    // Listen for clients:
    if(listen(socket_desc, 5) < 0){
        printf("Error while listening\n");
        return -1;
    }
    printf("Listening on port: %i\n", ntohs(server_addr.sin_port));
    printf("\nListening for incoming connections.....\n");
    
    
    do {
        // Accept an incoming connection:
        client_size = sizeof(client_addr);
        client_sock = accept(socket_desc, (struct sockaddr*)&client_addr, &client_size);
        if (client_sock < 0){
            printf("Can't accept\n");
            return -1;
        }
        printf("Client connected at IP: %s and port: %i\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        // Receive client's message:
        do {
            memset(client_message, '\0', sizeof(client_message));
            rval = read(client_sock, client_message, sizeof(client_message));
            if (rval < 0){
                printf("Couldn't receive, closing connection..\n");
                break;
            }
            if (rval == 0){
                printf("Nothing to read, closing connection..\n");
            }
            else {
                printf("Msg from client: %s\n", client_message);

                // Respond to client:

                if (send(client_sock, server_message, strlen(server_message), 0) < 0){
                    printf("Couldn't send response, closing connection..\n");
                    break;
                }
            }
        } while (rval > 0);

        // Closing the socket:
        close(client_sock);
    } while(1);
    close(socket_desc);
    
    return 0;
}
