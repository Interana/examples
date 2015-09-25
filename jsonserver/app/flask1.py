import os
import time
import ujson
from datetime import datetime

from flask import Flask, request
from flask import make_response
import gevent

app = Flask(__name__)

# Number of MB to force rotation after 5 second if bigger then this size
MAX_IMPORT_FILE_SIZE = 10 * 2 ** 20

# This is the minimum age to do a file size based flush
MIN_AGE = 5

# Number of seconds of last write time before closing file.  We should tune this to be customers * MAX_SECONDS
MAX_AGE = 30

BASE_DIR = os.path.join(os.path.dirname(__file__), "../logs/pipeline")

# This should ensure we cannot rotate a file onto the same name. (see MIN_AGE)
DT_FMT = "%Y%m%dT%H%M%S"
files_cache = {}


class ImportFile(object):
    def __init__(self, table_id, pipeline_id):
        self.fh = None
        self.customer_id = str(1)
        self.table_id = str(table_id)
        self.pipeline_id = str(pipeline_id)
        self.file_dir = os.path.join(BASE_DIR, 'completed', self.customer_id, self.table_id, self.pipeline_id)
        self.staging_dir = os.path.join(BASE_DIR, 'staging', self.customer_id, self.table_id, self.pipeline_id)

        if not os.path.isdir(self.file_dir):
            os.makedirs(self.file_dir)

        if not os.path.isdir(self.staging_dir):
            os.makedirs(self.staging_dir)

        # State of file on initiation
        self.file_len = None
        self.upload_start = None
        self.last_touch = None
        self.filename = None

    def new_file(self):
        self.close()
        self.file_len = 0
        self.upload_start = datetime.now()
        self.last_touch = self.upload_start
        self.filename = os.path.join(self.staging_dir, "tailer_" + self.upload_start.strftime(DT_FMT))
 

        self.fh = open(self.filename, 'a', 0)

    def should_rotate(self):

        age = (datetime.now() - self.upload_start).total_seconds()

        should_rotate = False
        if self.file_len > MAX_IMPORT_FILE_SIZE and age > MIN_AGE:
            should_rotate = True

        if age > MAX_AGE:
            should_rotate = True

        return should_rotate

    def write(self, data):
        """
        writes data to the appropriate file handle
        """
        if not self.fh:
            self.new_file()
            print "Opening {} {}".format(datetime.now(), self.fh)

        self.fh.write(data + '\r\n')
        self.fh.flush()
        self.last_touch = datetime.now()
        self.file_len = os.fstat(self.fh.fileno()).st_size

        if self.should_rotate():
            print "Rotating {} {}".format(datetime.now(), self.fh)
            self.new_file()

    def close(self):
        """
        closes a file handle
        """
        if self.fh:
            self.fh.flush()
            os.fsync(self.fh)
            #self.fh.fsync()
            self.fh.close()
            self.fh = None

    @classmethod
    def get_cache(cls, table_name, pipeline_id):
        cache_key = '{}_{}_{}'.format(1, table_name, pipeline_id)

        if cache_key not in files_cache:
            files_cache[cache_key] = ImportFile(table_name, pipeline_id)

        return files_cache[cache_key]


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
