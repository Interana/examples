import os
import time
import ujson
from datetime import datetime

from flask import Flask, request
from flask import make_response
import gevent

app = Flask(__name__)

def index():
    """
    Plain text
    """
    data = "This is the flask prototype application"
    rsp = make_response(data, 200)
    rsp.headers['Content-Type'] = "text/html"
    return rsp


@app.route('/test/perf/1')
def test_perf_1():
    """
    Basic return response json
    """
    response = {
        "message": "Great Scott, It works!!"
    }
    data = ujson.dumps(response)
    response_headers = [
        ('Content-type', 'application/json'),
        ('Content-Length', str(len(data)))
    ]
    rsp = make_response(data, 200)
    rsp.headers['Content-Type'] = "application/json"
    return rsp


@app.route('/test/perf/2')
def test_perf_2():
    """
    CPU intensive
    """
    number_of_rough_seconds = 7
    start = time.time()
    total_range = number_of_rough_seconds * pow(10, 7)
    x = 0
    for i in xrange(total_range):
        x += i * 2 % 13
    end = time.time()
    duration = end - start
    return "CPU Perf test_perf_2 finished in duration: %s" % duration


@app.route('/test/perf/3', defaults={'sleep': 0.05})
@app.route('/test/perf/3/<sleep>')
def test_perf_3(sleep):
    """
    Sleep for specified time
    """
    sleep = float(sleep)
    gevent.sleep(sleep)
    response = {
        "message": "CPU Perf test_perf_3 waited for {} ms".format(1000 * sleep)
    }
    data = ujson.dumps(response)
    rsp = make_response(data, 200)
    rsp.headers['Content-Type'] = "application/json"
    return rsp


@app.route('/test/perf/4', methods=['POST'])
def test_perf_4():
    """
    This is the performance test to append to a log file
    curl -H "Content-Type: application/text" -H "table: event" -H "pipeline_id: 1" -X POST -d '{"aaa" : 1}' "http://127.0.0.1:9090/test/perf/4"
    Assumptions : The data is decoded and is a json string (list not supported yet)
    """
    msg_dump = request.get_data()
    table_name = request.headers.get('table') or request.headers.get('table_name')
    pipeline_id = request.headers.get('pipeline_id')
    tailer_source_file = request.headers.get('tailer_source_file')
    len_msg = len(msg_dump) if msg_dump is not None else 0

    # print len_msg
    import_file = ImportFile.get_cache(table_name, pipeline_id)
    import_file.write(msg_dump)

    response = {
        "message": "Recieved message of size {} bytes".format(len_msg)
    }
    data = ujson.dumps(response)
    rsp = make_response(data, 200)
    rsp.headers['Content-Type'] = "application/json"
    return rsp


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9090, debug=True)
