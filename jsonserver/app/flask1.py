import time
import ujson
import cPickle

from flask import Flask
from flask import make_response
import gevent
import numpy

app = Flask(__name__)


@app.route('/')
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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9090)
