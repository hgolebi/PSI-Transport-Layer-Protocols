// Client side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT	 8080
#define MAXLINE 1024

struct msg {
    long int a;
    short int b;
    char c[10];
};

// Driver code
int main(int argc, char **argv) {
	int sockfd;
	char buffer[MAXLINE];
	struct sockaddr_in	 servaddr;
    struct msg send, *sendPtr;

	int n;
	socklen_t len;

    if (argc != 4) {
        printf("3 arguments required\n");
        return 1;
    }

	// Creating socket file descriptor
	if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}
    
	memset(&servaddr, 0, sizeof(servaddr));
	
	// Filling server information
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(PORT);
	servaddr.sin_addr.s_addr = INADDR_ANY;
    
    // arguments to struct
    send.a = atoi(argv[1]);
    send.b = atoi(argv[2]);
    strcpy(send.c, argv[3]);
    sendPtr = &send;
    
    sendto(sockfd, sendPtr, sizeof(send),
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,
            sizeof(servaddr));
    printf("Message sent.\n");
        
    n = recvfrom(sockfd, (char *)buffer, MAXLINE,
                MSG_WAITALL, (struct sockaddr *) &servaddr,
                &len);
    buffer[n] = '\0';
    printf("Server : %s\n", buffer); fflush(stdout);

	close(sockfd);
	return 0;
}
