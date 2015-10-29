#!/bin/bash
MY_PID=$$
echo Adding my pid to cgroup : $MY_PID
echo $MY_PID  | sudo tee /sys/fs/cgroup/memory/interana/cgroup.procs
for i in $(seq 1 100); do for j in $(seq 1 2); do (./memoryeater_and_kill 10 100 10 50 > memoryeater_and_kill.$i$j.log 2>&1  &) ; done ; sleep 30; done
