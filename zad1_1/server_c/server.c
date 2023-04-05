// Server side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define MAXLINE 1024

// Driver code
int main() {
	int sockfd;
	char buffer[MAXLINE];
	const char *hello = "Reply from server";
	struct sockaddr_in servaddr, cliaddr;

	socklen_t len;
    int sent_chars, recv_chars;

	// Creating socket file descriptor
	if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}

	memset(&servaddr, 0, sizeof(servaddr));
	memset(&cliaddr, 0, sizeof(cliaddr));

	// Filling server information
	servaddr.sin_family = AF_INET; // IPv4
	servaddr.sin_addr.s_addr = INADDR_ANY;
	servaddr.sin_port = 8080;

	// Bind the socket with the server address
	if ( bind(sockfd, (const struct sockaddr *)&servaddr,
			sizeof(servaddr)) < 0 )
	{
		perror("bind failed");
		exit(EXIT_FAILURE);
	}


	len = sizeof(cliaddr); //len is value/
	printf("Socket port #%d\n", ntohs(servaddr.sin_port));
    	while(1)
    	{
	recv_chars = recvfrom(sockfd, (char *)buffer, MAXLINE,
                    MSG_WAITALL, ( struct sockaddr *) &cliaddr,
                    &len);
		if (recv_chars < 0) {
			perror("something went wrong while receiving response");
			exit(EXIT_FAILURE);
		}
        buffer[recv_chars] = '\0';
        printf("Client (%s) : %s\n", inet_ntoa(cliaddr.sin_addr), buffer); fflush(stdout);

        sent_chars = sendto(sockfd, (const char *)hello, strlen(hello),
            MSG_CONFIRM, (const struct sockaddr *) &cliaddr,
                len);
		if (sent_chars != strlen(hello)) {
			perror("couldn't send the message");
			exit(EXIT_FAILURE);
		}
        printf("Reply sent.\n"); fflush(stdout);
    	}

	return 0;
}
