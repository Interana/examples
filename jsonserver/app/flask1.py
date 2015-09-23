import os
import time
import ujson
import datetime

from flask import Flask, request
from flask import make_response
import gevent
from gevent.lock import RLock

app = Flask(__name__)

MAX_IMPORT_FILE_SIZE = 10 * 2 ** 20  # 10 MB
BASE_DIR = os.path.join(os.path.dirname(__file__), "../logs/")
DT_FMT = "%Y%m%dT%H"
files_cache = {}
#lock = RLock()


class ImportFile(object):

    def __init__(self, customer_id, table_id, pipeline_id):
        self.fh = None
        self.customer_id = customer_id
        self.table_id = table_id
        self.pipeline_id = pipeline_id
        self.file_dir = os.path.join(BASE_DIR, 'pipeline', str(customer_id), str(table_id), str(pipeline_id))
        print "Creating {}".format(self.file_dir)
        if not os.path.isdir(self.file_dir):
            os.makedirs(self.file_dir)
        self.file_len = 0

    def new_file(self):
        self.close()
        self.last_touch = time.time()
        now = datetime.datetime.now()
        self.upload_start = datetime.datetime(now.year, now.month, now.day,
                                              now.hour, now.minute, now.second)

        self.filename = os.path.join(self.file_dir, "tailer_" + self.upload_start.strftime(DT_FMT))
        self.fh = open(self.filename, 'a', 0)
        self.file_len = 0

        # create inquisition or purify record
        # Create entry in data_sources.tailer_file table
        # print ("Added {filename} to tailer_file.  tailer_file_id: {tf_id}".format(filename=self.filename,
        #                                                                           tf_id=self.tailer_file_id))

    def write(self, data):
        """
        writes data to the appropriate file handle
        """
        if not self.fh:
            self.new_file()
            print "Opening {} {}".format(datetime.datetime.now(), self.fh)
        data_len = len(data)

        # if (self.upload_start.date() != datetime.date.today() or
        #                 data_len + self.file_len > MAX_IMPORT_FILE_SIZE):
        #     print "Rotating {} {}".format(datetime.datetime.now(), self.fh)
        #     self.new_file()

        #lock.acquire()
        self.fh.write(data + '\r\n')
        #self.fh.flush()
        #lock.release()
        self.last_touch = time.time()
        self.file_len = os.fstat(self.fh.fileno()).st_size

    def close(self):
        """
        closes a file handle
        """
        if self.fh:
            self.fh.close()
            self.fh = None

    @classmethod
    def get_cache(cls, table_name, pipeline_id):
        cache_key = '{}_{}_{}'.format(1, table_name, pipeline_id)

        if cache_key not in files_cache:
            files_cache[cache_key] = ImportFile(1, table_name, pipeline_id)

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
    """
    msg_dump = request.get_data()
    table_name = request.headers.get('table') or request.headers.get('table_name')
    pipeline_id = request.headers.get('pipeline_id')
    tailer_source_file = request.headers.get('tailer_source_file')
    len_msg = len(msg_dump) if msg_dump is not None else 0

    print len_msg
    import_file = ImportFile.get_cache(table_name, pipeline_id)
    import_file.write(msg_dump)

    #print "Passed in table={} pipeline_id={} tailer_source={} msg_len={}".format(table_name, pipeline_id,
    #                                                                             tailer_source_file, len_msg)

    response = {
        "message": "Recieved message of size {}".format(len_msg)
    }
    data = ujson.dumps(response)
    rsp = make_response(data, 200)
    rsp.headers['Content-Type'] = "application/json"
    return rsp


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9090, debug=False)
