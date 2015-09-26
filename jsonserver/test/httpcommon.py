import ujson
import requests


def http_session(base_url, pool_size=1000):
    block = False
    max_retries = 0

    http_pool_adapter = requests.adapters.HTTPAdapter(pool_size, pool_size, max_retries, block)

    session = requests.session()
    session.mount(base_url, http_pool_adapter)
    return session


g_rest_pool = None


def make_http_post_request(base_url, headers, data, timeout=5, max_retries=1):
    """
    A wrapper around BaseCaller. This is created so BaseCaller
    can run successfully inside a greenlet.
    :param payload:
    :return: return the payload and response back
    """

    retry_counter = 0
    response = None
    global g_rest_pool
    while response is None and retry_counter < max_retries:
        try:
            response = g_rest_pool.post(base_url,
                                        headers=headers,
                                        data=ujson.dumps(data),
                                        timeout=timeout)
        except Exception, e:
            print "Encountered Error {}".format(e)
            retry_counter += 1
    return response


def make_http_get_request(base_url, headers, params, timeout=5, max_retries=1):
    """
    A wrapper around BaseCaller. This is created so BaseCaller
    can run successfully inside a greenlet.
    :param payload:
    :return: return the payload and response back
    """

    retry_counter = 0
    response = None
    global g_rest_pool
    while response is None and retry_counter < max_retries:
        try:
            response = g_rest_pool.get(base_url,
                                     headers=headers,
                                     params=params,
                                     timeout=timeout)
        except Exception, e:
            print "Encountered Error {}".format(e)
            retry_counter += 1
    return response