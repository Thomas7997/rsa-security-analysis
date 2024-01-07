#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define ROOT_FOLDER "./keys"

int main (int argc, char ** argv) {
	if (argc != 3) {
		printf("Arguments invalides. Vous dever renseigner le nombre de clés à générer et leur taille.\n");
	}

	int nkeys = atoi(argv[1]);

	for (int i = 0; i < nkeys; i++) {
		char * cmd = calloc(150, sizeof(char));
		sprintf(cmd, "openssl genrsa -out %s-%s/rsa-%d.out %s", ROOT_FOLDER, argv[2], i, argv[2]);
		system(cmd);
		free(cmd);
	}

	printf("Clés RSA correctement générées !\n");
	
	return 0;
}