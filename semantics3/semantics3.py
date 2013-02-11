import json
import oauth2 as oauth
import urllib
API_DOMAIN = 'api.semantics3.com'
API_BASE = 'https://'+API_DOMAIN+'/v1/'

class Semantics3Request:
	def __init__(self, api_key=None, api_secret=None, endpoint=None):
		self.endpoint     = endpoint
		self.api_key      = api_key
		self.api_secret   = api_secret
		self.consumer     = oauth.Consumer(api_key,api_secret)
		self.access_token = oauth.Token('', '')
		self.client       = oauth.Client(self.consumer,self.access_token)

		self.data_query   = {}
		self.query_result = None

	def fetch(self,endpoint,params):
		api_endpoint = API_BASE + endpoint + '?' + urllib.urlencode({'q':params})	
		resp, content = self.client.request( api_endpoint, 'GET' )
		return content 

	def remove(self, endpoint, *fields):
		def _remove(path, hash):
			if len(path) == 1:
				del hash[path[0]]
			else:
				_remove(path[1:],hash[path[0]])
				if not hash[path[0]]:
					del hash[path[0]]
		_remove(fields,self.data_query[endpoint])

	def add(self, endpoint, *fields):
		ancestors = fields[:-2]
		parent = self.data_query.setdefault(endpoint, {})
		for i in ancestors:
			parent = parent.setdefault(i, {}) 
		parent[fields[-2]] = fields[-1]
	
	def field(self, *fields):
		self.add(self.endpoint, *fields)

	def cache(self, cache_size):
		self.cache_size = cache_size 
	def iter(self):
		self.add(self.endpoint, 'limit', self.cache_size)
		self.run_query()
		if( 'total_results_count' in self.query_result ):
			offset = 0
			total_count = self.query_result['total_results_count']
			while( offset < total_count ):
				for i in self.query_result['results']:
					yield i
				offset = offset + len(self.query_result['results'])
				self.add(self.endpoint, 'offset', offset)
				if( offset < total_count ): self.run_query()

	def query(self, endpoint, **kwargs):
		return json.loads(self.fetch(endpoint,json.dumps(kwargs)))

	def run_query(self, endpoint = None):
		endpoint = endpoint or self.endpoint
		query = self.data_query[endpoint]
		self.query_result = self.query(
			endpoint,
			**query
		)
	def get(self, endpoint = None):
		self.run_query(endpoint)
		return self.query_result

	def clear_query(self):
		self.data_query = {}
		self.query_result = {}
