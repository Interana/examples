import gevent
from gevent import monkey as curious_george
from gevent.pool import Pool
curious_george.patch_all(thread=False, select=False)

import argparse
from collections import defaultdict
from datetime import datetime
import time
import ujson
import urlparse


DEFAULT_HEADERS = {
    'Content-type': "html/text",
    # 'Accept-Encoding': "gzip"
}

BASE_PATH = '/test/perf/4'

from httpcommon import http_session
from httpcommon import make_http_post_request


def request_generator(host_port, duration=1.0, rate_sec=100, burst_sec=1.0, num_columns=100, parallize=True):
    """
    This generates data and dispatches on a greenlet.  It uses a window to keep the rate constant
    :return:
    """
    base_url =  urlparse.urljoin(host_port, BASE_PATH)
    burst_size = int(rate_sec * burst_sec)
    start = datetime.now()
    total = duration * rate_sec
    total_loops = int(duration / burst_sec)

    string_to_int_ratio = 0.20
    string_columns = int(num_columns * string_to_int_ratio)
    int_columns = num_columns - string_columns

    basic_data = {'column_int_{}'.format(x): x for x in xrange(int_columns)}
    basic_data = dict(basic_data.items() +
                      {'column_string_{}'.format(x): "column_value_{}".format(x) for x in
                       xrange(string_columns)}.items())

    basic_data['_id'] = 0

    basic_data_list = [basic_data.copy() for x in xrange(burst_size)]

    total_size = len(ujson.dumps(basic_data))

    headers = {'table': 'event',
               'pipelineid': '1'}

    headers = dict(headers.items() + DEFAULT_HEADERS.items())

    print "Total size of post {}".format(total_size)

    total_code_count = defaultdict(int)
    total_elapsed = {'max': -1e9, 'min': 1e9, 'sum': 0, 'rps': 0}

    pool = Pool(burst_size + burst_size)
    import httpcommon

    httpcommon.g_rest_pool = http_session(base_url, burst_size + burst_size)

    for loop in range(total_loops):
        greenlets = []
        for burst_id in range(burst_size):
            basic_data_list[burst_id]['_id'] = burst_id
            greenlets.append(
                pool.spawn(make_http_post_request, base_url,  headers, basic_data_list[burst_id], timeout=10, max_retries=1))
        start_1 = time.time()
        gevent.joinall(greenlets)
        results = [g.value for g in greenlets]
        end_1 = time.time()
        duration = end_1 - start_1

        current_code_count = defaultdict(int)
        elapsed_list = []

        for r in results:
            if r is not None:
                current_code_count[r.status_code] += 1
                total_code_count[r.status_code] += 1
                elapsed_list.append(r.elapsed.total_seconds())
            else:
                current_code_count['-1'] += 1
                total_code_count['-1'] += 1
        current_elapsed = {'max': max(elapsed_list), 'min': min(elapsed_list),
                           'avg': 1.0 * sum(elapsed_list) / len(elapsed_list),
                           'sum': sum(elapsed_list), 'rps': len(elapsed_list) / duration}

        print "* Loop {} Total Time({}), result {}, timing {}".format(loop, duration, dict(current_code_count.items()),
                                                                      current_elapsed)
        total_elapsed['max'] = max([total_elapsed['max'], current_elapsed['max']])
        total_elapsed['min'] = min([total_elapsed['min'], current_elapsed['min']])
        total_elapsed['sum'] = sum([total_elapsed['sum'], current_elapsed['sum']])
        total_elapsed['rps'] = sum([total_elapsed['rps'], current_elapsed['rps']])

    total_elapsed['avg'] = total_elapsed['sum'] / (1.0 * sum(total_code_count.values()))
    total_elapsed['rps'] = total_elapsed['rps'] / (1.0 * total_loops)

    return total_code_count, total_elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Load test for realistic post data",
        epilog="""This should validate that all segments are written to file.
        """)

    sleep_time = 0.5

    parser.add_argument('-H', '--host_port', help='The host and port to do load test, i.e. http://127.0.0.1:9090',
                        default='http://127.0.0.1:9090')


    parser.add_argument('-a', '--action', help='Do a test run or check results',
                        default='run', choices=['run', 'check'])

    parser.add_argument('-d', '--duration', help='The duration of test',
                        default=1, type=int)

    parser.add_argument('-b', '--burst_duration', help='The duration of each burst',
                        default=1, type=int)

    parser.add_argument('-r', '--rate', help='The request per second to target',
                        default=1000, type=int)

    parser.add_argument('-c', '--columns', help='The number of columns',
                        default=100, type=int)

    args = parser.parse_args()

    if args.action == 'run':
        start_1 = time.time()
        result, total_elapsed = request_generator(args.host_port, args.duration, args.rate, args.burst_duration, args.columns)
        end_1 = time.time()
        duration = (end_1 - start_1)

        total_errors = sum([val for code, val in result.iteritems() if code != 200])
        total_cnt = sum(result.values())

        print "+++All Result {}, Error Rate {} %".format(result, 100.0 * total_errors / (total_cnt * 1.0))
        print "+++Total Time: ({}) host={} Parallel={} elapsed {}".format(
            duration, args.host_port, args.rate, total_elapsed)


if __name__ == "__main__":
    main()
