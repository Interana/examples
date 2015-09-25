echo New Test > load_gen_out.log
for x in `seq 1 $1`; do nohup sh -c 'python -u load_gen_grequest.py -p 2000 -l 10 -u http://127.0.0.1:9090/test/perf/3/0.5 &' 2>&1 >> load_gen_out.log  ; done
