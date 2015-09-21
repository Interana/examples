from collections import defaultdict
import time
import grequests
import argparse
from pprint import pprint

def grequest_handler(base_url, num_parallel, num_loop):
    urls = [base_url for i in range(num_parallel)]

    total_code_count = defaultdict(int)
    total_elapsed = {'max' : -1e9, 'min' : 1e9, 'sum' : 0, 'rps' : 0}
    for loop in range(num_loop):
        start_1 = time.time()
        rs = (grequests.get(u) for u in urls)
        res = grequests.map(rs)
        current_code_count = defaultdict(int)
        current_elapsed = {}
        elapsed_list = []
        
        end_1 = time.time()
        duration = end_1 - start_1
 
        for r in res:
            if r is not None:
                current_code_count[r.status_code] += 1
                total_code_count[r.status_code] += 1 
                elapsed_list.append(r.elapsed.total_seconds ())                
            else:
                current_code_count[None] += 1           
        current_elapsed = {'max': max(elapsed_list), 'min': min(elapsed_list), 'avg' : 1.0 * sum(elapsed_list)/len(elapsed_list), 
                           'sum' : sum(elapsed_list), 'rps': len(elapsed_list)/duration}
        print "* Loop {} Total Time({}), result {}, timing {}".format(loop, duration, dict(current_code_count.items()), current_elapsed)
        total_elapsed['max'] = max([total_elapsed['max'], current_elapsed['max']])
        total_elapsed['min'] = min([total_elapsed['min'], current_elapsed['min']])
        total_elapsed['sum'] = sum([total_elapsed['sum'], current_elapsed['sum']])
        total_elapsed['rps'] = sum([total_elapsed['rps'], current_elapsed['rps']])

    total_elapsed['avg'] = total_elapsed['sum'] / (1.0 * sum(total_code_count.values()))
    total_elapsed['rps'] = total_elapsed['rps'] / (1.0 * num_loop)

    return total_code_count, total_elapsed


def main():

    parser = argparse.ArgumentParser(
        description="Load test for jsonserver",
        epilog="""ex.
T1:
T2:
T3:
""")


    sleep_time = 0.5
 
    parser.add_argument('-u', '--url', help='The url to load test',
                        default='http://127.0.0.1:9090/test/perf/3/{}'.format(sleep_time))

    parser.add_argument('-l', '--loops', help='The number of loops',
                        default=1, type=int)
 
    parser.add_argument('-p', '--parallel', help='The number of parallel url calls to make',
                        default=1000, type=int)
      

    args = parser.parse_args()
    
    start_1 = time.time()
    result, total_elapsed = grequest_handler(args.url, args.parallel, args.loops)
    end_1 = time.time()
    duration = (end_1 - start_1)

    total_errors = sum([val for code, val in result.iteritems() if code != 200])
    total_cnt = sum(result.values())

    print "+++All Result {}, Error Rate {} %".format(result, 100.0 * total_errors/(total_cnt * 1.0))
    print "+++Total Time: ({}) url={} Parallel={} elapsed {}".format (
        duration, args.url, args.parallel, total_elapsed)


if __name__ == "__main__":
    main()
 