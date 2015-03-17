#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define MB 1048576
#define CONSUME 10 * MB
#define THREADS 1000
#define LOOPS 100

void eat();

int main(int argc, char *argv[])
{
    pthread_t lol[10000];
    int i;
    for(i = 0; i < THREADS; i++)
    {
        pthread_create(&lol[i], NULL, eat, NULL);

        //Simple memory allocation using malloc
//        char *lol = malloc(CONSUME);
//        memset(lol, 1, CONSUME);
//        printf("Theads, %d iterations\n",i);
    }
    sleep(3600);
}

void eat()
{
    //time to fuck shit up.
    //pid_t childPID;
    //childPID = fork();
    while(1)
    {
        int i;
        for(i = 0; i < LOOPS ; i++)
        {
            char *lol = malloc(CONSUME);
            memset(lol, 1, CONSUME);
            printf("Theads, %d iterations\n",i);
        }
        sleep(3600);
        
    }
}
