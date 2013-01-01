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
		self.query_result = self.query("products",
				cat_id = 4992,
				brand  = "Toshiba"
				)
		pp.pprint(self.query_result)

