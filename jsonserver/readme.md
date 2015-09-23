

## Dependencies

sudo apt-get install nginx
sudo apt-get install libev-dev
sudo apt-get install libevent-devel

## Install nginx and change user to "interana" assuming that all the settings from our build has been applied




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

## Build httperf
```
sudo apt-get install build-essential autoconf automake bison flex libtool intltool

git clone git@github.com:klueska/httperf.git
vim /usr/include/x86_64-linux-gnu/bits/typesizes.h >> change FS_SET to 65535

cd httperf
autoreconf -i
automake --add-missing
mkdir -p httperf/build && cd httperf/build
../configure
make
```

## TBD
## httperf
sudo apt-get install httperf

## Test Nginx\System using httperf at 100K connections per second (100K rps)
./src/httperf --hog --timeout=1 --client=0/1 --server=127.0.0.1 --port=80 --uri=/ --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=10000 --num-calls=100
pkill -9 -f httperf

## Run Connection Test using httperf (1K rps)
/src/httperf --hog --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/3/0.5 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=10000 --num-calls=1
pkill -9 -f httperf


## Run ConnctionTest + persistent connections (2K rps)
./src/httperf --hog --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/3/0.5 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=1000 --num-calls=10
pkill -9 -f httperf


## Run ConnectionTest using test driver (800 rps)
python -u load_gen_grequest.py -p 5000 -l 5 -u http://127.0.0.1:9090/test/perf/3/0.5

## Run Tailer test using test driver (300 rps)
python -u load_tailer_service.py -d 6 -b 2 -r 1000 -c 1000
python -u load_tailer_service.py -d 6 -b 2 -r 1000 -c 10000




# Known Issues


1) All Performance should be done with your "laptop" plugged in in high power mode or else you will get signficantly degraded numbers

2) 
