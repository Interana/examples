echo New Test > load_gen_out.log


if [ -z "$2" ] ; then
    for x in `seq 1 $1`; do nohup sh -c 'python -u load_gen_grequest.py -p 2000 -l 10 -u http://127.0.0.1:9090/test/perf/3/0.5 &' 2>&1 >> load_gen_out.log  ; done
else
    export TEST_URL=$2
    for x in `seq 1 $1`; do nohup sh -c 'python -u load_gen_grequest.py -p 2000 -l 10 -u $TEST_URL &' 2>&1 >> load_gen_out.log  ; done
fi
