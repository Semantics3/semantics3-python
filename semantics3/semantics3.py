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

        oauth_request = oauth.OAuthRequest.from_consumer_and_token( self.consumer, token=self.access_token, http_method='GET', http_url = api_endpoint, parameters = {'q': params})
        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), self.consumer, self.access_token)
        connection = httplib.HTTPSConnection(API_DOMAIN)

        api_request_url = oauth_request.to_url()
        connection.request(oauth_request.http_method, api_request_url)
        response = connection.getresponse()
        
        return response.read()
        #print "Request status: %s" % response.status
        #print "Request response: %s" % response.read()

class Products(Semantics3Request):
    def __init__(self, api_key,api_secret):
        Semantics3Request.__init__(self,api_key,api_secret)

        self.products_query = {}
        self.categories_query = {}
        self.query_result = {}

    def test(self):
        pp = pprint.PrettyPrinter(indent=4)
        self.query_result = json.loads(Semantics3Request.fetch(self,"products",'{"cat_id":4992,"brand":"Toshiba"}'))
        pp.pprint(self.query_result)

#    #Categories
#
#    def category_field(field_name,field_value):
#        @@categories_query[field_name] = field_value
#
#    def get_categories
#      _run_query("categories",@@categories_query)
#      @@query_result
#    end
#
#    #Products
#
#    def products_field(*fields)
#      pquery = @@products_query
#      flen = fields.length
#      #check if flen is >1
#      prev = fields[0]
#      cur = fields[0]
#      for i in 1..(flen-1)
#        cur = fields[i]
#        if not pquery.has_key?(prev)
#          pquery[prev] = {}
#        end
#        if i == (flen-1)
#          pquery[prev] = cur
#        else
#          if not pquery[prev].has_key?(cur)
#            pquery[prev][cur] = {}
#          end
#        end
#        pquery = pquery[prev] #move up one level
#        prev = cur
#      end
#      puts @@products_query.inspect
#    end
#
#
##    def sitedetails(field_name,field_value1,*field_value2):
##      products_field("sitedetails",field_name,field_value1,*field_value2)
#
##    def latestoffers(field_name,field_value1,field_value2):
##      products_field("sitedetails","latestoffers",field_name,field_value1,*field_value2)
#
#    def limit(limit):
#      products_field("limit",limit)
#
#    def offset(offset):
#      products_field("offset",offset)
#
#    def sort_list(sort_field,sort_value):
#      products_field("sort",sort_field,sort_value)
#
#    def get_products:
#      _run_query("products",@@products_query)
#      @@query_result
#
#    def iter:
#      if not @@query_result.has_key?(total_results_count) or @@query_result['offset'] >= @@query_result['total_results_count']
#        #die
#      end 
#      limit = MAX_LIMIT
#      if @@products_query.has_key?('limit')
#        limit = @@products_query['limit']
#      end 
#      @@products_query['offset'] = @@query_result['offset'] + limit
#      get_products()
#
#    def all_products
#      if not @@query_result.has_key?(results)
#        #die
#      end
#      @@query_result['results']
#    end
#
#    #General
#
#    def query(endpoint,hash_ref={})
#      _run_query(endpoint,hash_ref)
#      @@query_result
#    end
#
#    def query_json(endpoint,json_str)
#      _run_query(endpoint,JSON.parse(json_str))
#      @@query_result
#    end
#
#    def clear_query
#      @@categories_query={}
#      @@products_query={}
#      @@query_result={}
#    end
#
#    private
#
#    def _run_query(endpoint,query_ref={})
#      @@query_result = _make_request(endpoint,query_ref.to_json)
#    end




