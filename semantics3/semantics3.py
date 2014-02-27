import json
from requests_oauthlib import OAuth1Session

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

try:
    from .error import Semantics3Error
except ImportError:
    from error import Semantics3Error


API_DOMAIN = 'api.semantics3.com'
API_BASE = 'https://' + API_DOMAIN + '/v1/'


class Semantics3Request:

    def __init__(self, api_key=None, api_secret=None, endpoint=None):
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

    def fetch(self, endpoint, params):
        api_endpoint = API_BASE + endpoint + '?' +\
            urllib.urlencode({'q': params})
        content = self.oauth.get(api_endpoint,headers={'User-Agent':'Semantics3 Python Lib/0.2'})
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
                    'Cannot add this constraint, \'' + parent + '\' is already\
                                                                    a value.'
                )

        if isinstance(parent, dict):
            parent[fields[-2]] = fields[-1]
        else:
            raise Semantics3Error(
                'Invalid constraint',
                'Cannot add this constraint, \'' + parent + '\' is already\
                                                                a value.'
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

    def query(self, endpoint, **kwargs):
        content = self.fetch(endpoint, json.dumps(kwargs)).content.decode('utf-8')
        return json.loads(content)

    def run_query(self, endpoint=None):
        endpoint = endpoint or self.endpoint
        if not endpoint in self.data_query:
            raise Semantics3Error("No query built", "You need to first create\
                                            a query using the add() method.")
        query = self.data_query[endpoint]
        self.query_result = self.query(
            endpoint,
            **query
        )

        if self.query_result['code'] != 'OK':
            raise Semantics3Error(self.query_result['code'],
                                  self.query_result['message'])

    def get(self, endpoint=None):
        self.run_query(endpoint)
        return self.query_result

    def clear_query(self):
        self.data_query = {}
        self.query_result = {}
