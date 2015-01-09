# semantics3
semantics3 is a python client for accessing the Semantics3 Products API, which provides structured information, including pricing histories, for a large number of products.
See https://www.semantics3.com for more information.

API documentation can be found at https://www.semantics3.com/docs/

## Installation
semantics3 can be installed through pip:

```bash
pip install semantics3
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
You can access your API access credentials from the user dashboard at https://www.semantics3.com/dashboard/applications

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
    
```

### UPC Query

Running a UPC/EAN/GTIN query is as simple as running a search query:

```python
# Build the request
sem3.products_field("upc", "883974958450")
sem3.products_field("field", ["name","gtins"])

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


