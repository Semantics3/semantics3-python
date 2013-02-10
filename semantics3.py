import json
from oauth import oauth
import httplib
import pprint

API_DOMAIN = 'api.semantics3.com'
API_BASE = 'https://'+API_DOMAIN+'/v1/'

class Semantics3Request:
	def __init__(self, api_key=None, api_secret=None, endpoint=None):
		self.api_key = api_key
		self.api_secret = api_secret
		self.consumer = oauth.OAuthConsumer(api_key,api_secret)
		self.access_token = oauth.OAuthToken('', '')
		self.endpoint     = endpoint
		self.data_query   = {}
		self.query_result = None

	def fetch(self, endpoint, params):
		api_endpoint = API_BASE + endpoint

		oauth_request = oauth.OAuthRequest.from_consumer_and_token(
				self.consumer,
				token       = self.access_token,
				http_method = 'GET',
				http_url    = api_endpoint,
				parameters  = {'q': params}
			)
		oauth_request.sign_request(
				oauth.OAuthSignatureMethod_HMAC_SHA1(),
				self.consumer,
				self.access_token
			)
		connection = httplib.HTTPSConnection(API_DOMAIN)

		api_request_url = oauth_request.to_url()
		connection.request(oauth_request.http_method, api_request_url)
		response = connection.getresponse()

		return response.read()
		#print "Request status: %s" % response.status
		#print "Request response: %s" % response.read()

	def remove_field(self, endpoint, *fields):
		def remove(path, hash):
			if len(path) == 1:
				del hash[path[0]]
			else:
				remove(path[1:],hash[path[0]])
				if not hash[path[0]]:
					del hash[path[0]]
		remove(fields,self.data_query[endpoint])

	def add(self, endpoint, *fields):
		ancestors = fields[:-2]
		parent = self.data_query.setdefault(endpoint,{})
		for i in ancestors:
			parent = parent.setdefault(i, {}) 
		parent[fields[-2]] = fields[-1]

	def query(self, endpoint, **kwargs):
		return json.loads(self.fetch(json.dumps(kwargs),endpoint))

	def run_query(self, endpoint):
		self.query_result = self.query(
			endpoint,
			**self.data_query[endpoint]
		)

	def field(self, *fields):
		self.add(self.endpoint, *fields)

	def get(self):
		self.run_query(self.endpoint)
		return self.query_result

	def clear_query(self):
		self.data_query = {}
		self.query_result = {}
