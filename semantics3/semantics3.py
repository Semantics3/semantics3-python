import json
from oauth import oauth
import httplib
import pprint
#error handling

API_DOMAIN = 'api.semantics3.com'
API_BASE = 'https://'+API_DOMAIN+'/v1/'

class Semantics3Request(object):

	def __init__(self, api_key=None, api_secret=None):
		self.api_key = api_key
		self.api_secret = api_secret
		self.consumer = oauth.OAuthConsumer(api_key,api_secret)
		self.access_token = oauth.OAuthToken('', '')

	def fetch(self,endpoint,params):
		api_endpoint = API_BASE + endpoint

		oauth_request = oauth.OAuthRequest.from_consumer_and_token(
				self.consumer,
				token=self.access_token,
				http_method='GET',
				http_url = api_endpoint,
				parameters = {'q': params}
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
	def query(self, endpoint,**kwargs):
		return json.loads(self.fetch(endpoint,json.dumps(kwargs)))

class Products(Semantics3Request):
	def __init__(self, api_key,api_secret):
		Semantics3Request.__init__(self,api_key,api_secret)

		self.products_query = {}
		self.categories_query = {}
		self.query_result = {}


	def test(self):
		pp = pprint.PrettyPrinter(indent=4)
		#self.query_result = json.loads(Semantics3Request.fetch(self,"products",'{"cat_id":4992,"brand":"Toshiba"}'))
		"""
		self.query_result = self.query("products",
				cat_id = 4992,
				brand  = "Toshiba"
			)
		pp.pprint(self.query_result)
		"""
		self.products_field('test1','test2','test3')
		self.products_field('test2','test2','test3')
		self.products_field('test2','test4','test3')
		self.products_field('test1','test3','test4')
		self.products_field('test3','val3','test4')
		print self.products_query

	def category_field(self, field_name, field_value):
		self.categories_query[field_name] = field_value

	def get_categories(self):
		self._run_query("categories", self.categories_query)
		return self.query_result
	
	def get_products(self):
		self._run_query("products", self.products_query)
		return self.query_result

	def products_field(self, *fields):
		ancestors = fields[:-2]
		parent = self.products_query
		for i in ancestors:
			parent = parent.setdefault(i, {}) 
		parent[fields[-2]] = fields[-1]

	def sitedetails(self, field_name, field_value1, *field_value2):
		self.products_field(
				"sitedetails", 
				field_name,
				field_value1,
				*field_value2
			)

	def latestoffers(self, field_name, field_value1, field_value2):
		self.products_field(
				"sitedetails",
				"latestoffers",
				field_name,
				field_value1,
				*field_value2
			)

	def limit(self, limit):
		self.products_field("limit",limit)
	
	def offset(self, offset):
		self.products_field("offset",offset)
	
	def sort_list(self, sort_field, sort_value):
		self.products_field("sort", sort_field, sort_value)

	def iter(self):
		pass
	
	
	def query_json(self, endpoint, json_str):
		self._run_query(endpoint, json.loads(json_str))
		return self.query_result

	def clear_query(self):
		self.categories_query = {}
		self.products = {}
		self.query_result = {}

	def _run_query(self, endpoint, query_ref={}):
		self.query_result = self.query(endpoint, **query_ref)

