#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]){

    fprintf(stdout, "Test of executing the CGI in the Server Venturini/1.1.\n");
    fprintf(stdout, "This executable was write in C in the Fri, Apr 27.\n");
    fprintf(stdout, "Bellow, see the query if you has write:\n\n");

    if(argc == 1){
        fprintf( stdout, "No has query params.\n");
    } else if(argc > 1){

        int i;
        for(i = 0; i < argc; i ++){
            fprintf(stdout, argv[i]);
            fprintf(stdout, "\n");
        }
        fprintf(stdout, "\n");
    }

    fprintf(stdout, "End of program.\n");
    return 0;
}
