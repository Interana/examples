import ujson
import gevent


def application(environ, start_response):
    status = '200 OK'
    """
    Sleep for specified time
    """
    sleep = 0.5
    sleep = float(sleep)
    gevent.sleep(sleep)
    response = {
        "message": "CPU Perf test_perf_3 waited for {} ms".format(1000 * sleep)
    }
    output = ujson.dumps(response)
    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)
    return [output]
