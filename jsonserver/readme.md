## Ultra Json Server

A low latency event driven server utilizing nginx/uwsgi and python flask api

## Dependencies and nginx install
```
sudo apt-get install python-dev python-pip nginx libev-dev libev4 libpcre3 libpcre3-dev httperf
```

## Update the system config (note this will destroy your interana config)

```
cd conf/etc
sudo mkdir -p /etc/default
sudo cp -r default/* /etc/default/
sudo cp -r nginx/* /etc/nginx/
sudo cp -r pam.d/* /etc/pam.d/
sudo cp -r security/* /etc/security/
sudo cp  sysctl.conf /etc/
sudo ln -s /etc/nginx/sites-available/jsonserver1.com /etc/nginx/sites-enabled/jsonserver1.com
sudo sysctl -p
```

# TBD update the nginx site-avaialable and ad the internal ip


# Add Socket file as below and give it world permissions (tbd do we need?)
```
touch /tmp/uwsgi
chown interana:interana /tmp/uwsgi
chmod 777 /tmp/uwsgi
```

## Install libraries using virtualenv

sudo pip install virtualenv
sudo pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv jsonserver
workon jsonserver
pip install -r requirements.txt
pip install -r requirements_test.txt

## Run uwsgi server with a ini file for the config
```
sudo /etc/init.d/nginx restart
cd rest && uwsgi uwsgi-laptop.ini
```

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

## Various Monitors
htop
sudo iostat -dmx 5
watch -n 1 -d "sudo netstat -antpu | awk '{print \$6}' | sort | uniq -c"
sudo iftop -i eth0




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
cd test
./load_gen_request.sh 10



## Run Tailer write to file test, 26K blocks * 10K rps (T2)
cd test
./load_tailer_service.sh 5


# Known Issues


1) All Performance should be done with your "laptop" plugged in in high power mode or else you will get signficantly degraded numbers

2) HTTP Perf will shows errors on FD-Unavailable : that is a bug with httperf that can be ignored

3) Sometime the ulimits do not apply correctly.  You may get "Max Files limit reached". To test this use return-limits macro
return-limits uwsgi

```
return-limits(){

     for process in $@; do
          process_pids=`sudo ps -C $process -o pid --no-headers | cut -d " " -f 2`

          if [ -z $@ ]; then
             echo "[no $process running]"
          else
             for pid in $process_pids; do
                   echo "[$process #$pid -- limits]"
                   cat /proc/$pid/limits
             done
          fi

     done

}
```

# How to deploy onto an existing Interana cluster

0) On Import nodes, setup to use the squid proxy for apt-get and pip

/etc/apt/apt.conf
```
Acquire {
        Retries "0";
        HTTP {
                Proxy "http://10.0.0.210:1933";
        };
};
```

For pip use the --proxy flag
```
pip install --proxy=http://10.0.0.210:1933 <name of module>
```
                                                                                                                                                                                       
For git update the ~/.ssh/config file
```
Host github.com
    User                    git
    ProxyCommand            ssh -q -A interana@push000  nc  %h %p
                                                                   
```                    


1) Copy git package onto import node

2) Copy nginx conf onto upstreams

3) Add a /etc/init.d/ia-nginx

4) Follow steps above to deploy nginx

5) Ensure that logs/pipeline is linked to the SSD or else there will be large variance in performance

6) Run test with ip, i.e.

./load_gen_request.sh 10 "http://10.0.1.48:9090/test/perf/3/0.5"
./load_tailer_service.sh 1 http://10.0.1.48:9090



