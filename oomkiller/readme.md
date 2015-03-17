Memory Eater Script


# Description

The simple memory eater is good bait for the linux OOM Killer
It runs threads and consume memories, then it just sleeps and holds malloc'd memory

OOM Kills are loged various places, usually kern.log
grep -ie "oom" /var/log/*.lo




The script can be built as follows
gcc -o2 memoryeater.c -o memoryeater -pthread -std=c99


# Steps

1) 1 thread and allocate 1 GB of memory, in 10 MB chunks
./memoryeater 10 1 100


2) Run a fork bomb loop with 1 thread
for i in $(seq 1 2); do for j in $(seq 1 50); do (./memoryeater 10 1 100 &)  ; done ; sleep 10; done


3) Run with 100 threads and allocate 10 GB of memory
./memoryeater 10 100 100


4) Fork Bomb + threads, 10G
for i in $(seq 1 5); do for j in $(seq 1 2); do (./memoryeater 10 100 10 &)  ; done ; sleep 10; done


5) Duration test

for i in $(seq 1 100); do for j in $(seq 1 5); do (./memoryeater 10 100 10 &)  ; done ; sleep 10; done


6) Thread kill and stuff - Duration test

for i in $(seq 1 100); do for j in $(seq 1 5); do (./memoryeater_and_kill 10 100 10 50 &)  ; done ; sleep 30; done



#Results

Kernel 3.11.0-12-generic
1) OK
2) OK
3) HANG 1/20
4) HANG 1/20
5) HANG 1/5 


Kernel 3.13.0-44-generic

1) OK
2) OK
3) OK
4) OK
5) HANG 1/5

Kernel 3.14.4-031404-generic

1) OK
2) OK
3) OK
4) OK
5) HANG 1/5


# Patch Details

It seems that linux has problems trying to OOM kill a set of threads/lwp under a parent process if they all
have memory pressure

https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=0c740d0afc3bff0a097ad03a1c8df92757516f5c

This seems to be deployed in v3.14.

~/build/linux(master) $ git tag --contains 0c740d0afc3bff0a097ad03a1c8df92757516f5c
v3.14
v3.14-rc1
v3.14-rc2
v3.14-rc3
v3.14-rc4
v3.14-rc5
v3.14-rc6
v3.14-rc7
v3.14-rc8
v3.15
v3.15-rc1
v3.15-rc2
v3.15-rc3
v3.15-rc4
v3.15-rc5
v3.15-rc6
v3.15-rc7
v3.15-rc8
v3.16
v3.16-rc1
v3.16-rc2
v3.16-rc3
v3.16-rc4
v3.16-rc5
v3.16-rc6
v3.16-rc7
v3.17
v3.17-rc1
v3.17-rc2
v3.17-rc3
v3.17-rc4
v3.17-rc5
v3.17-rc6
v3.17-rc7
v3.18
v3.18-rc1
v3.18-rc2
v3.18-rc3
v3.18-rc4
v3.18-rc5
v3.18-rc6
v3.18-rc7
v3.19
v3.19-rc1
v3.19-rc2
v3.19-rc3
v3.19-rc4
v3.19-rc5
v3.19-rc6
v3.19-rc7
v4.0-rc1
v4.0-rc2
v4.0-rc3
v4.0-rc4