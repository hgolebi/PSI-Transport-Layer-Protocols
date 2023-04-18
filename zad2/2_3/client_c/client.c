#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <fcntl.h>
#include <errno.h>


int main(int argc, char **argv)
{
    int socket_desc;
    struct sockaddr_in server_addr;
    char server_message[2000], client_message[2000];
    struct hostent *hp, *gethostbyname();
    char *aip;

    // Clean buffers:
    memset(server_message,'\0',sizeof(server_message));
    memset(client_message,'\0',sizeof(client_message));
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    
    if(socket_desc < 0){
        printf("Unable to create socket\n");
        return -1;
    }

    // Setting socket to non-blocking mode:
    int flags, ret;

    flags = fcntl(socket_desc, F_GETFL, 0);
    if (flags == -1) {
        return -1;
    }

    flags |= O_NONBLOCK;
    ret = fcntl(socket_desc, F_SETFL, flags);
    if (ret == -1) {
        return -1;
    }
    
    printf("Socket created successfully\n");
    
    // Set port and IP the same as server-side:
    server_addr.sin_family = AF_INET;
    // server_addr.sin_port = htons(8000);
    // server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (argc != 3) {
        printf("Wrong number of arguments. Please insert 2 arguments.\n");
        return -1;
    }
    hp = gethostbyname(argv[1]);
    if (hp == 0) {
        printf("Couldn't resolve given address\n");
        return -1;
    }
    char *endptr;
    int port;
	port = strtol(argv[2], &endptr, 10);
    if (port <= 0) {
        printf("Given port was wrong.\n");
        return -1;
    }
	memcpy((char *) &server_addr.sin_addr, (char *) hp->h_addr, hp->h_length);
	aip = inet_ntoa( *((struct in_addr*) hp->h_addr_list[0]));
	
    // int po = atoi(argv[2]);
	printf("Server IP: %s:%d\n", aip, port);
	server_addr.sin_port = htons(port);
    

    // Send connection request to server:
    if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        if (errno != EINPROGRESS){
            perror("Unable to connect\n");
            return -1;
        }
        fd_set write_fds;
        struct timeval timeout;
        
        FD_ZERO(&write_fds);
        FD_SET(socket_desc, &write_fds);

        timeout.tv_sec = 5; // 5 seconds timeout

        int retval;
        retval = select(socket_desc + 1, NULL, &write_fds, NULL, &timeout);
        if (retval == 0) {
            printf("Connection timed out.\n");
            return -1;
        }
        if (retval < 0) {
            perror("Unable to connect\n");
            return -1;
        }
    }

    // Get input from the user:
    printf("Enter message: ");
    gets(client_message);
    
    
    // Send the message to server:
    if(send(socket_desc, client_message, strlen(client_message), 0) < 0){
        perror("Unable to send message\n");
        return -1;
    }
    
    // Checking if socket is ready to read
    fd_set read_fds;
    struct timeval timeout;
    
    FD_ZERO(&read_fds);
    FD_SET(socket_desc, &read_fds);

    timeout.tv_sec = 5; // 5 seconds timeout

    int retval;
    retval = select(socket_desc + 1, &read_fds, NULL, NULL, &timeout);
    if (retval == 0) {
        printf("Connection timed out.\n");
        return -1;
    }
    if (retval < 0) {
        perror("Error while receiving server's response\n");
        return -1;
    }
    
    // Receive the server's response:
    if(read(socket_desc, server_message, sizeof(server_message)) < 0){
        perror("Error while receiving server's response\n");
        return -1;
    }
    
    printf("Server's response: %s\n",server_message);
    
    // Close the socket:
    close(socket_desc);
    
    return 0;
}

