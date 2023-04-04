// Client side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

#define PORT	 8080
#define MAXLINE 1024

// Driver code
int main(int argc, char **argv) {
	int sockfd;
	char buffer[MAXLINE];
	const char *hello = "Hello from client";
	struct sockaddr_in	 servaddr;
	struct hostent *hp, *gethostbyname();
	char *aip;

	printf("Starting");
    int i, num_msg = 1;

	int sent_chars, recv_chars;
	socklen_t len;

    if (argc > 1) {
        num_msg = atoi(argv[1]);
    }
    	/*
	if (argc > 2) {
		hello = argv[2];
	}
	*/

	// Creating socket file descriptor
	if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}
	/*

	memset(&servaddr, 0, sizeof(servaddr));

	// Filling server information
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(PORT);
	servaddr.sin_addr.s_addr = INADDR_ANY;

	*/
	hp = gethostbyname(argv[2]);
	
	memcpy((char *) &servaddr.sin_addr, (char *) hp->h_addr, hp->h_length);
	aip = inet_ntoa( *((struct in_addr*) hp->h_addr_list[0]));
	printf("Server IP: %s\n", aip);
	servaddr.sin_port = htons(atoi(argv[3]));

	for (i = 0; i < num_msg; i = i+1)
    {
        sent_chars = sendto(sockfd, (const char *)hello, strlen(hello),
            MSG_CONFIRM, (const struct sockaddr *) &servaddr,
                sizeof(servaddr));
		if (sent_chars != strlen(hello)) {
			perror("couldn't send the message");
			exit(EXIT_FAILURE);
		}
        printf("Hello message sent.\n");

        recv_chars = recvfrom(sockfd, (char *)buffer, MAXLINE,
                    MSG_WAITALL, (struct sockaddr *) &servaddr,
                    &len);
		if (recv_chars < 0) {
			perror("something went wrong while receiving response");
			exit(EXIT_FAILURE);
		}
        buffer[recv_chars] = '\0';
        printf("Server : %s\n", buffer); fflush(stdout);
    }

	if (close(sockfd) < 0) {
		perror("couldn't close file descriptor");
		exit(EXIT_FAILURE);
	}
	return 0;
}
