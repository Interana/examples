## Install nginx and change user to "interana"


## Chmod uswgi socket

chown interana:jag /tmp/uwsgi
chmod 777 /tmp/uwsgi



## Update the max files

sudo vim /etc/security/limits.conf
interana soft nofile 1000000
interana hard nofile 1000000

ulimit -aS



## Update somaxconn

echo 4096 > /proc/sys/net/core/somaxconn

vim /etc/sysctl.conf
net.core.somaxconn=4096



## Run uwsgi
cd rest && uwsgi <name_of_ini>


## Run connection test. 
python -u test/load_gen_grequest.py -p 5000 -l 5 -u http://127.0.0.1:9090/test/perf/3/0.5


## Run using httperf
sudo apt-get install httperf
httperf --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/3/0.5 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=10000 --num-calls=1


## Run http pipelining
httperf --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/3/0.5 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=100000 --num-calls=10
