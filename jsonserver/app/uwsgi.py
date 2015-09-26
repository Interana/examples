import re
import ujson

# def application(environ, start_response):
#     status = '200 OK'
#     """
#     Sleep for specified time
#     """
#     sleep = 0.5
#     sleep = float(sleep)
#     gevent.sleep(sleep)
#     response = {
#         "message": "CPU Perf test_perf_3 waited for {} ms".format(1000 * sleep)
#     }
#     output = ujson.dumps(response)
#     response_headers = [('Content-type', 'application/json'),
#                         ('Content-Length', str(len(output)))]
#
#     start_response(status, response_headers)
#     return [output]
import gevent
from common import ImportFile


def not_found(environ, start_response):
    start_response('404 Not Found', [('content-type','text/html')])
    return []

def get_all_headers(environ):

    headers = {}
    for key, value in environ.iteritems():
        if 'HTTP_' in key:
            headers[key[5:].lower()] = value

    return headers

def index(environ, start_response):
    test_perf_1(environ, start_response)

def test_perf_1(environ, start_response):
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
    start_response('200 OK', response_headers)
    return data



def test_perf_3(environ, start_response, sleep=0.05):
    """
    Sleep for specified time
    """
    sleep = float(sleep)
    gevent.sleep(sleep)
    response = {
        "message": "CPU Perf test_perf_3 waited for {} ms".format(1000 * sleep)
    }
    data = ujson.dumps(response)
    response_headers = [
        ('Content-type', 'application/json'),
        ('Content-Length', str(len(data)))
    ]

    start_response('200 OK', response_headers)
    return data


def test_perf_4(environ, start_response):
    """
    This is the performance test to append to a log file
    curl -H "Content-Type: application/text" -H "table: event" -H "pipeline_id: 1" -X POST -d '{"aaa" : 1}' "http://127.0.0.1:9090/test/perf/4"
    Assumptions : The data is decoded and is a json string (list not supported yet)
    """

    headers = get_all_headers(environ)
    table_name = headers.get('table') or headers.get('table_name')
    pipeline_id = headers.get('pipeline_id')
    tailer_source_file = headers.get('tailer_source_file')

    msg_dump = None
    try:
        len_msg = int(environ.get('CONTENT_LENGTH', '0'))
        msg_dump = environ['wsgi.input'].read(len_msg)
    except ValueError:
        len_msg = 0

    # print len_msg
    import_file = ImportFile.get_cache(table_name, pipeline_id)
    import_file.write(msg_dump)

    response = {
        "message": "Recieved message of size {} bytes".format(len_msg)
    }
    data = ujson.dumps(response)
    response_headers = [
       ('Content-type', 'application/json'),
       ('Content-Length', str(len(data)))
    ]

    start_response('200 OK', response_headers)
    return data


## Put routes down here to the message above.  When having parameter, always put all variants in there
urls = [
    (r'^$', index),
    (r'test/perf/1/?$', test_perf_1),
    (r'test/perf/3/(\d.\d+)/?$', test_perf_3),
    (r'test/perf/3/?$', test_perf_3),
    (r'test/perf/4/?$', test_perf_4)
]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            params = match.groups()
            if len(params) == 0:
                return callback(environ, start_response)
            else:
                return callback(environ, start_response, *params)
    return not_found(environ, start_response)


if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 9090, application)
    srv.serve_forever()
