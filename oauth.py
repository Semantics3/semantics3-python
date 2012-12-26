from oauth import oauth
import httplib
 
consumer_key = 'INSERT_API_KEY'
consumer_secret = 'INSERT_API_SECRET'
api_endpoint = 'https://api.semantics3.com/v1/products'
consumer = oauth.OAuthConsumer(consumer_key,consumer_secret)
access_token = oauth.OAuthToken('', '')
oauth_request = oauth.OAuthRequest.from_consumer_and_token(
    consumer,
    token=access_token,
    http_method='GET',
    http_url = api_endpoint,
    parameters = {'q': '{"brand":"Toshiba","cat_id":13658}'})
oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                           consumer, access_token)

connection = httplib.HTTPSConnection('api.semantics3.com')
api_request_url = oauth_request.to_url()
connection.request(oauth_request.http_method, api_request_url)
response = connection.getresponse()
 
print "Request status: %s" % response.status
print "Request response: %s" % response.read()

