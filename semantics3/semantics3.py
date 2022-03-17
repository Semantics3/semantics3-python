import re
import time
import json
import logging

from requests_oauthlib import OAuth1Session
from url_normalize import url_normalize
#from urllib3.exceptions import HTTPError, ProtocolError
from requests.exceptions import ConnectionError, RequestException

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

try:
    from .error import Semantics3Error
except ImportError:
    from error import Semantics3Error


class Semantics3Request:

    def __init__(self, api_key=None, api_secret=None, endpoint=None, api_base='https://api.semantics3.com/v1/', timeout=120):
        if api_key is None:
            raise Semantics3Error(
                'API Credentials Missing',
                'You did not supply an api_key. Please sign up at\
                https://semantics3.com/ to obtain your api_key.'
            )
        if api_secret is None:
            raise Semantics3Error(
                'API Credentials Missing',
                'You did not supply an api_secret. Please sign up at\
                https://semantics3.com/ to obtain your api_key.'
            )
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint
        self.oauth = OAuth1Session(api_key, client_secret=api_secret)
        self.data_query = {}
        self.query_result = None
        self.cache_size = 10
        self.api_base = api_base
        self.timeout = timeout
        self.oauth_session_start = int(time.time())

    def fetch(self, method, endpoint, params):
        api_endpoint = url_normalize(self.api_base + endpoint)
        if method.lower() in ['get', 'delete']:
            content = self.oauth.request(
                        method,
                        api_endpoint,
                        params = params,
                        headers={'User-Agent':'Semantics3 Python Lib/0.2'},
                        timeout=self.timeout
                    )
        else:
            content = self.oauth.request(
                        method,
                        api_endpoint,
                        data = json.dumps(params),
                        headers={'User-Agent':'Semantics3 Python Lib/0.2', 'Content-Type':'application/json'},
                        timeout=self.timeout
                    )
        return content

    def remove(self, endpoint, *fields):
        def _remove(path, hash):
            if path[0] in hash:
                if len(path) == 1:
                    del hash[path[0]]
                else:
                    _remove(path[1:], hash[path[0]])
                    if not hash[path[0]]:
                        del hash[path[0]]
            else:
                raise Semantics3Error(
                    'Constraint does not exist',
                    "Constraint '" + path[0] + "' does not exist."
                )
        _remove(fields, self.data_query[endpoint])

    def add(self, endpoint, *fields):
        ancestors = fields[:-2]
        parent = self.data_query.setdefault(endpoint, {})
        for i in ancestors:
            if isinstance(parent, dict):
                parent = parent.setdefault(i, {})
            else:
                raise Semantics3Error(
                    'Invalid constraint',
                    'Cannot add this constraint, \'' + parent + '\' is already a value.'
                )

        if isinstance(parent, dict):
            parent[fields[-2]] = fields[-1]
        else:
            raise Semantics3Error(
                'Invalid constraint',
                'Cannot add this constraint, \'' + parent + '\' is already a value.'
            )

    def field(self, *fields):
        self.add(self.endpoint, *fields)

    def cache(self, cache_size):
        self.cache_size = cache_size

    def iter(self):
        self.add(self.endpoint, 'limit', self.cache_size)
        self.run_query()
        if('total_results_count' in self.query_result):
            offset = 0
            total_count = self.query_result['total_results_count']
            while(offset < total_count):
                for i in self.query_result['results']:
                    yield i
                offset = offset + len(self.query_result['results'])
                self.add(self.endpoint, 'offset', offset)
                if(offset < total_count):
                    self.run_query()

    def _reinitialize_client(self):
        duration = int(time.time()) - self.oauth_session_start
        logging.debug("Encountered connection error. Duration since client created: {d}s, Recreating semantics3 client".format(d=duration))
        self.oauth.close() #-- Close connection pool associated with current session
        self.__init__() #-- Initiate new client

    def query(self, method, endpoint, kwargs, retry_attempt=0):
        if method.lower() == "get":
            params = { 'q' : json.dumps(kwargs) }
        else:
            params = kwargs

        #-- Following is a patch/hack made to circumvent issues encountered during
        #-- migrating sem3 infra to k8s sem3stage and sem3prod clusters accordingly
        #-- however this doesn't address the root cause, it only bypass the issue by retries on client side
        #-- it performs auto retry (upto 1 attempt) whenever we encounter following errors
        
        #-- Everytime we receive either of the following errors, retry the request
        #-- 1. Connection reset by peer
        try:
            response = self.fetch(method, endpoint, params)
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError, RequestException) as e:
            err_str = str(e)
            if retry_attempt <= 1 and re.search("Connection (?:aborted|reset by peer)", err_str):
                logging.debug(err_str)
                self._reinitialize_client()
                return self.query(method, endpoint, kwargs, retry_attempt+1)
            elif retry_attempt > 1:
                logging.debug("Exceeded max retry attempts, Skipping. Error: {e}".format(e=str(e)))
            else:
                logging.debug("Encountered unknown error: {e}".format(e=str(e)))

        
        #-- 2. Gateway timeout (status code 504) error retry
        if response.status_code == 504:
            if retry_attempt <= 1:
                logging.debug("Encountered a gateway timeout error, Sending the request again")
                return self.query(method, endpoint, kwargs, retry_attempt+1)
            else:
                logging.debug("Encountered a gateway timeout error, Exceeded max retry attempts, Skipping")
        
        #-- Check if response received is a malformed json
        try:
            response_json = response.json()
        except:
            raise Exception("Malformed JSON")

        if response.status_code < 400:
            return response.json()
        else:
            if response.json().get('code') != 'OK':
                response_body = response.json()
                raise Semantics3Error(response_body.get('code'),
                                      response_body.get('message'))

    def run_query(self, endpoint=None, method='GET', params=None):
        endpoint = endpoint or self.endpoint
        if method.lower() == "get":
            try:
                query = self.data_query[endpoint]
            except KeyError:
                query = params or {}
            self.query_result = self.query(
                method,
                endpoint,
                query
            )
        else:
            self.query_result = self.query(
                method,
                endpoint,
                params
            )
        return self.query_result

    def get(self, endpoint=None):
        return self.run_query(endpoint)

    def clear_query(self):
        self.data_query = {}
        self.query_result = {}
