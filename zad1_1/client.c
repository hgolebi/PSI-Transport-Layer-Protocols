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

// Driver code
int main(int argc, char **argv) {
	int sockfd;
	char buffer[MAXLINE];
	const char *hello = "Hello from client";
	struct sockaddr_in	 servaddr;

    int i, num_msg;

	int sent_chars, recv_chars;
	socklen_t len;

    if (argc > 1) {
        num_msg = atoi(argv[1]);
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
