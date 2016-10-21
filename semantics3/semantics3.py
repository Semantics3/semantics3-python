import json
from requests_oauthlib import OAuth1Session
from urltools import normalize

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

try:
    from .error import Semantics3Error
except ImportError:
    from error import Semantics3Error


class Semantics3Request:

    def __init__(self, api_key=None, api_secret=None, endpoint=None, api_base='https://api.semantics3.com/v1/'):
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

    def fetch(self, method, endpoint, params):
        api_endpoint = normalize(self.api_base + endpoint)
        if method.lower() in ['get', 'delete']:
            content = self.oauth.request(
                        method,
                        api_endpoint,
                        params = params,
                        headers={'User-Agent':'Semantics3 Python Lib/0.2'}
                      )
        else:
            content = self.oauth.request(
                        method,
                        api_endpoint,
                        data = json.dumps(params),
                        headers={'User-Agent':'Semantics3 Python Lib/0.2', 'Content-Type':'application/json'}
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

    def query(self, method, endpoint, kwargs):
        if method.lower() == "get":
            params = { 'q' : json.dumps(kwargs) }
        else:
            params = kwargs
        response = self.fetch(method, endpoint, params)
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
