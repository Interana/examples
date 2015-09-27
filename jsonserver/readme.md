## Ultra Json Server

A low latency event driven server utilizing nginx/uwsgi and python flask api

## Dependencies and nginx install
```
sudo apt-get install nginx
sudo apt-get install libev-dev
sudo apt-get uninstall libevent-devel
```

## Update the system config (note this will destroy your interana config)

```
cd conf
cp -r default/ /etc/default/
cp -r nginx/ /etc/nginx/
cp -r pam.d /etc/pam.d/
cp -r security/ security/
cp  sysctl.conf /etc/

sudo sysctl -p
```

# TBD update the nginx site-avaialable and ad the internal ip


# Add Socket file as below and give it world permissions (tbd do we need?)
```
chown interana:interana /tmp/uwsgi
chmod 777 /tmp/uwsgi
```

## Run uwsgi server with a ini file for the config
```
cd rest && uwsgi flask1-laptop.ini
```



## Alternatively install via debian
sudo apt-get install httperf


## Build httperf (TBD, doesnt work well just skip)
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

## Refer to this confluence page to record results for T0, T1 and T2 using the config file
For the python test there are many test cases fired off, so you need to sum from log file all the RPSs together
grep +++ load_gen_out.log

## Test Connection Test using Nginx\System 100K rps (T0)
httperf --hog --timeout=1 --client=0/1 --server=127.0.0.1 --port=80 --uri=/ --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=10000 --num-calls=100
pkill -9 -f httperf

## Run Connection Test using httperf 1K rps (T1)
httperf --hog --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/1 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=10000 --num-calls=100
pkill -9 -f httperf


## Run ConnctionTest using httperf 2K persistent rps
httperf --hog --timeout=5 --client=0/1 --server=127.0.0.1 --port=9090 --uri=/test/perf/3/0.5 --rate=1000 --send-buffer=4096 --recv-buffer=16384 --num-conns=1000 --num-calls=10
pkill -9 -f httperf


## Run Max rps
./load_gen_request.sh 10



## Run Tailer write to file test (T2)
./load_tailer_service.sh 5


# Known Issues


1) All Performance should be done with your "laptop" plugged in in high power mode or else you will get signficantly degraded numbers

2) HTTP Perf will shows errors on FD-Unavailable : that is a bug with httperf that can be ignored

3) 
