#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define MB 1048576

int CONSUME; // Pass in the alloc size in MB
int THREADS; // Number of total threads to alloc
int LOOPS;  // The number of loops
int KILLPCT; // The percentage of threads to kill, 0% means we just create all threads linearly.


typedef struct thread_params_ {
    int thread_id;

} THREAD_PARAMS;


void * memeater(void *data_ptr)
{
    srand(time(NULL));
    THREAD_PARAMS *t_param = ((THREAD_PARAMS*) data_ptr);
    int thread_id = t_param->thread_id;
    while(1)
    {
        int i;
        for(i = 0; i < LOOPS ; i++) {
            char *lol = malloc(CONSUME);
            memset(lol, 1, CONSUME);
            printf("Theads %d, iterations %d malloc\n", thread_id, i);
        }
        free(data_ptr);

        int r = rand() % 100;
        if (KILLPCT > r){
            printf("Theads %d, killing\n", thread_id);
            pthread_exit(0);
        }
        else {
            printf("Theads %d, sleeping\n", thread_id);
            sleep(3600);

        }

    }
}

int main(int argc, char *argv[])
{


    setvbuf(stdout, NULL, _IONBF, 0);

    if (argc != 5)
    {
        printf("Found %d args  Must have 4 args Usage %s <CONSUME_MB> <THREADS> <LOOPS_PER_THREAD> <KILL_PERCENT>", argc-1, argv[0]);
        exit(1);
    }

    CONSUME = atoi(argv[1])*MB;
    THREADS = atoi(argv[2]);
    LOOPS = atoi(argv[3]);
    KILLPCT = atoi(argv[4]);

    pthread_t pt_array[10000];
    float KILLRATIO = ((float)KILLPCT)/100.0;
    int remaining = THREADS;
    int tid = 0;
    while (remaining > 0) {
        int next_alloc_group = (int)(KILLRATIO * remaining);
        if (next_alloc_group == 0) {
            next_alloc_group = 1;
        }
        int i;
        for (i=0; i < next_alloc_group; i++){
            THREAD_PARAMS *t_args = malloc(sizeof(THREAD_PARAMS));
            tid += 1;
            t_args->thread_id =tid;
            pthread_create(&pt_array[i], NULL, memeater, t_args);
        }
        remaining -= next_alloc_group;
        printf("MAIN LOOP SLEEPING..");
        sleep((next_alloc_group/10));

    }
    sleep(3600);
}


