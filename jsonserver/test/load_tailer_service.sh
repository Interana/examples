echo New Test > load_tailer_out.log


if [ -z "$2" ] ; then

    for x in `seq 1 $1`; do nohup sh -c 'python -u load_tailer_service.py -d 10 -b 1 -r 2000 -c 1000 &' 2>&1 >> load_tailer_out.log  ; done
else
    export HOST_PORT="$2"
    for x in `seq 1 $1`; do nohup sh -c 'python -u load_tailer_service.py -d 10 -b 1 -r 2000 -c 1000 -H $HOST_PORT &' 2>&1 >> load_tailer_out.log  ; done
fi
