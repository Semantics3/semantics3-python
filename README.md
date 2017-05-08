# semantics3
semantics3 is a python client for accessing the Semantics3 Products API, which provides structured information, including pricing histories, for a large number of products.
See https://www.semantics3.com for more information.

API documentation can be found at https://www.semantics3.com/docs/

## Installation
semantics3 can be installed through pip:

```bash
pip install semantics3
```

To install the egg directly from github

```bash
pip install -e git+ssh://git@github.com/Semantics3/semantics3-python.git#egg=semantics3
```

To install the latest source:

```bash
git clone https://github.com/Semantics3/semantics3-python.git
cd semantics3-python
python setup.py install
```

## Requirements
* requests-oauthlib

## Getting Started

In order to use the client, you must have both an API key and an API secret. To obtain your key and secret, you need to first create an account at
https://www.semantics3.com/
You can access your API access credentials from the user dashboard at https://dashboard.semantics3.com.

### Setup Work

Let's lay the groundwork.

```python
from semantics3 import Products

# Set up a client to talk to the Semantics3 API using your Semantics3 API Credentials
sem3 = Products(
	api_key = "SEM3xxxxxxxxxxxxxxxxxxxxxx",
	api_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)
```

### First Request aka 'Hello World':

Let's run our first request! We are going to run a simple search for the word "iPhone" as follows:


```python
# Build the request
sem3.products_field("search", "iphone")

# Run the request
results = sem3.get_products()
#or
results = sem3.get()

# View the results of the request
print results
```

## Sample Requests

The following examples show you how to interface with some of the core functionality of the Semantics3 Products API.

### Pagination

The example in our "Hello World" script returns the first 10 results. In this example, we'll scroll to subsequent pages, beyond our initial request:

```python
# Build the request
sem3.products_field("search", "iphone")

# Run the request
results = sem3.get_products()

# Specify a cache size
sem3.cache(5)

# Iterate through the results
page_no = 0
for i in sem3.iter():
    page_no += 1
	print "We are at page = %s" % page_no
    print "The results for this page are:"
    print i
    sleep(1) #respect rate limit
```

### UPC Query

Running a UPC/EAN/GTIN query is as simple as running a search query:

```python
# Build the request
sem3.products_field("upc", "883974958450")
sem3.products_field("fields", ["name","gtins"])

# Run the request
results = sem3.get_products()

# View the results of the request
print results 
```

### URL Query

Get the picture? You can run URL queries as follows:

```python
sem3.products_field("url", "http://www.walmart.com/ip/15833173")
results = sem3.get_products()
print results
```

### Price Filter

Filter by price using the "lt" (less than) tag:

```python
sem3.products_field("search", "iphone")
sem3.products_field("price", "lt", 300)
results = sem3.get_products()
print results
```

### Category ID Query

To lookup details about a cat_id, run your request against the categories resource:

```python
# Build the request
sem3.categories_field("cat_id", 4992)

# Run the request
results = sem3.get_categories()

# View the results of the request
print results
```

## Webhooks
You can use webhooks to get near-real-time price updates from Semantics3.

### Creating a webhook

You can register a webhook with Semantics3 by sending a POST request to `"webhooks"` endpoint.
To verify that your URL is active, a GET request will be sent to your server with a `verification_code` parameter. Your server should respond with `verification_code` in the response body to complete the verification process.

```python
params = {
    webhook_uri : "http://mydomain.com/webhooks-callback-url"
}

webhook = sem3.run_query("webhooks", "POST", params)
print webhook["id"]
print webhook["webhook_uri"]
```

To fetch existing webhooks
```python
webhooks = sem3.run_query("webhooks", "GET")
print webhooks
```

To remove a webhook
```python
webhook_id = '7JcGN81u'
endpoint = "webhooks/%s" % webhook_id

response = sem3.run_query( endpoint, "DELETE")
print response
```

### Registering events
Once you register a webhook, you can start adding events to it. Semantics3 server will send you notifications when these events occur.
To register events for a specific webhook send a POST request to the `"webhooks/{webhook_id}/events"` endpoint

```python
params = {
    "type": "price.change",
    "product": {
        "sem3_id": "1QZC8wchX62eCYS2CACmka"
    },
    "constraints": {
        "gte": 10,
        "lte": 100
    }
}

webhook_id = '7JcGN81u'
endpoint = "webhooks/%s/events" % webhook_id

eventObject = sem3.run_query(endpoint,  "POST", params)
print eventObject["id"]
print eventObject["type"]
print eventObject["product"]
```

To fetch all registered events for a give webhook
```python
webhook_id = '7JcGN81u'
endpoint = "webhooks/%s/events" % webhook_id

events = sem3.run_query(endpoint,  "GET")
print events
```

### Webhook Notifications
Once you have created a webhook and registered events on it, notifications will be sent to your registered webhook URI via a POST request when the corresponding events occur. Make sure that your server can accept POST requests. Here is how a sample notification object looks like
```javascript
{
    "type": "price.change",
    "event_id": "XyZgOZ5q",
    "notification_id": "X4jsdDsW",
    "changes": [{
        "site": "abc.com",
        "url": "http://www.abc.com/def",
        "previous_price": 45.50,
        "current_price": 41.00
    }, {
        "site": "walmart.com",
        "url": "http://www.walmart.com/ip/20671263",
        "previous_price": 34.00,
        "current_price": 42.00
    }]
}
```
## Contributing
Use GitHub's standard fork/commit/pull-request cycle.  If you have any questions, email <support@semantics3.com>.

## Authors

* Shawn Tan

* Abishek Bhat <abishek@semantics3.com>

## Copyright

Copyright (c) 2015 Semantics3 Inc.

## License

    The "MIT" License
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.


