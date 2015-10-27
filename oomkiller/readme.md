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
```
./memoryeater 10 1 100
```


2) Run a fork bomb loop with 1 thread
```
for i in $(seq 1 2); do for j in $(seq 1 50); do (./memoryeater 10 1 100 &)  ; done ; sleep 10; done
```

3) Run with 100 threads and allocate 10 GB of memory
```
./memoryeater 10 100 100
```


4) Fork Bomb + threads, 10G
```
for i in $(seq 1 5); do for j in $(seq 1 2); do (./memoryeater 10 100 10 &)  ; done ; sleep 10; done
```


5) Heavy Preasure test, just hammer it with 100 threads * 5 process
```
for i in $(seq 1 100); do for j in $(seq 1 5); do (./memoryeater 10 100 10 &)  ; done ; sleep 30; done
```


6) Thread kill and stuff - Duration test.  Light Pressure and thread restarts
```
for i in $(seq 1 100); do for j in $(seq 1 10); do (./memoryeater_and_kill 10 10 10 50 &)  ; done ; sleep 30; done
```


7) Thread kill and stuff - Duration test.  Using 100 threads, Heavy Pressure and threads restart
```
for i in $(seq 1 100); do for j in $(seq 1 2); do (./memoryeater_and_kill 10 100 10 50 &)  ; done ; sleep 30; done
```

8) Super heavy
```
for i in $(seq 1 100); do for j in $(seq 1 10); do (./memoryeater_and_kill 10 100 10 50 &)  ; done ; sleep 30; done
```

8) Other ideas
```
cgroups
overcommit
```


#Results

Kernel 3.11.0-12-generic
```
1) OK
2) OK
3) HANG 1/20
4) HANG 1/20
5) HANG 1/5 
6) OK  
7) Hang 1/4
```

Kernel 3.14.4-031404-generic
```
1) OK
2) OK
3) OK
4) OK
5) HANG 1/5
6) OK
7) HANG 1/20
```

Kernel 3.18.9-031809-generic
```
6) OK
7) HANG 1/100
```

Kernel 3.18.9-031809-generic - with oom flag
```
6) OK
7) OK
```



# How to install new Kernel (3.18.9)
```
mkdir ubuntu-3.18.9
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.18.9-vivid/linux-headers-3.18.9-031809-generic_3.18.9-031809.201503080036_amd64.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.18.9-vivid/linux-headers-3.18.9-031809_3.18.9-031809.201503080036_all.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.18.9-vivid/linux-image-3.18.9-031809-generic_3.18.9-031809.201503080036_amd64.deb
sudo dpkg -i *.deb
>>> Install Package Maintainers Version (Grub)
sudo update-grub
vim /boot/grub/menu.lst
```



# How to OOM Flag

1) Check flag
```
sudo cat /proc/sys/vm/oom_kill_allocating_task
```

2) Update
```
echo 1 | sudo tee /proc/sys/vm/oom_kill_allocating_task
```

3) Verify
```
sudo cat /proc/sys/vm/oom_kill_allocating_task
```

4) Permanize
```
sudo vim /etc/sysctl.conf
vm.oom_kill_allocating_task = 0
```


Note: For the test above, this will kill the shell of your test.  To get around this you need
to put in a ./sh script and run
```
nohup memoryeater.sh &
```

# Cgroups
```
sudo apt-get install cgroup-bin
sudo cgcreate -a ubuntu:ubuntu -t ubuntu:ubuntu -g memory:ubuntu
memLimit = 5,000,000
echo export /sys/fs/cgroup/memory/interana/memory.limit_in_bytes' % memLimit
PID-
echo PID > /sys/fs/cgroup/memory/interana/cgroup.procs
```

NOTE: for newer kernels, you must turn on memory cgroup (due its overhead)
```
ubuntu@ip-10-158-142-183:~$ sudo vim /etc/default/grub
ubuntu@ip-10-158-142-183:~$ sudo update-grub
```



# Patch Details

It seems that linux has problems trying to OOM kill a set of threads/lwp under a parent process if they all
have memory pressure

https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=0c740d0afc3bff0a097ad03a1c8df92757516f5c

This seems to be deployed in v3.14.

~/build/linux(master) $ git tag --contains 0c740d0afc3bff0a097ad03a1c8df92757516f5c
```
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
....
```
