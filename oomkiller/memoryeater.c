#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define MB 1048576

int CONSUME;
int THREADS;
int LOOPS;


void * memeater(void *data_ptr)
{
    int a = *((int *) data_ptr);
    while(1)
    {
        int i;
        for(i = 0; i < LOOPS ; i++)
        {
            char *lol = malloc(CONSUME);
            memset(lol, 1, CONSUME);
            printf("Theads %d, iterations %d\n", (int)a, i);
        }
        sleep(3600);

    }
}

int main(int argc, char *argv[])
{

    if (argc != 4)
    {
        printf("Found %d args  Must have 3 args Usage %s <CONSUME_MB> <THREADS> <LOOPS_PER_THREAD>", argc-1, argv[0]);
        exit(1);
    }

    CONSUME = atoi(argv[1])*MB;
    THREADS = atoi(argv[2]);
    LOOPS = atoi(argv[3]);

    pthread_t pt_array[10000];
    for(int i = 0; i < THREADS; i++)
    {

        int *t_arg = malloc(sizeof(*t_arg));
        *t_arg = i;
        pthread_create(&pt_array[i], NULL, memeater, t_arg);

    }
    sleep(3600);
}


