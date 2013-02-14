semantics3
==========

semantics3 is a python client for accessing the Semantics3 Products API,
which provides structured information, including pricing histories, for
a large number of products. See https://www.semantics3.com for more
information.

Quickstart guide: https://www.semantics3.com/quickstart API
documentation can be found at https://www.semantics3.com/docs/

Installation
------------

semantics3 can be installed through pypi:

::

    pip install semantics3

To install the latest source from the repository

::

    git clone https://github.com/Semantics3/semantics3-python.git
    cd semantics3-python
    python setup.py install

Requirements
------------

-  oauth2

Getting Started
---------------

In order to use the client, you must have both an API key and an API
secret. To obtain your key and secret, you need to first create an
account at https://www.semantics3.com/ You can access your API access
credentials from the user dashboard at
https://www.semantics3.com/dashboard/applications

Setup Work
~~~~~~~~~~

Let's lay the groundwork.

::

    from semantics3 import Products

    # Set up a client to talk to the Semantics3 API using your Semantics3 API Credentials
    products = Products(
        api_key = "SEM3xxxxxxxxxxxxxxxxxxxxxx",
        api_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )

First Query aka 'Hello World':
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's make our first query! For this query, we are going to search for
all Toshiba products that fall under the category of "Computers and
Accessories", whose cat\_id is 4992.

::

    # Build the query
    products.products_field( "cat_id", 4992 )
    products.products_field( "brand", "Toshiba" )

    # Make the query
    results = products.get_products();
    #or
    results = products.get()

    # View the results of the query
    print results

Examples
--------

The following examples show you how to interface with some of the core
functionality of the Semantics3 Products API. For more detailed examples
check out the Quickstart guide: https://www.semantics3.com/quickstart

Explore the Category Tree
~~~~~~~~~~~~~~~~~~~~~~~~~

In this example we are going to be accessing the categories endpoint. We
are going to be specifically exploiring the "Computers and Accessories"
category, which has a cat\_id of 4992. For more details regarding our
category tree and associated cat\_ids check out our API docs at
https://www.semantics3.com/docs

::

    # Build the query
    products.categories_field( "cat_id", 4992 );

    # Execute the query
    results = products.get_categories();

    # View the results of the query
    print results

Nested Search Query
~~~~~~~~~~~~~~~~~~~

You can intuitively construct all your complex queries but just
repeatedly using the products\_field() or add() methods. Here is how we
translate the following JSON query:

::

    {
        "cat_id" : 4992, 
        "brand"  : "Toshiba",
        "weight" : { "gte":1000000, "lt":1500000 },
        "sitedetails" : {
            "name" : "amazon.com",
            "latestoffers" : {
                "currency": "USD",
                "price"   : { "gte" : 100 } 
            }
        }
    }

This query returns all Toshiba products within a certain weight range
narrowed down to just those that retailed recently on amazon.com for >=
USD 100.

::

    # Build the query
    products = Products( api_key, api_secret )
    products.products_field( "cat_id", 4992 )
    products.products_field( "brand", "Toshiba" )
    products.products_field( "weight", "gte", 1000000 )
    products.products_field( "weight", "lt", 1500000 )
    products.products_field( "sitedetails", "name", "amazon.com" )
    products.products_field( "sitedetails", "latestoffers", "currency", "USD" )
    products.products_field( "sitedetails", "latestoffers", "price", "gte", 100 )
    # Let's make a modification - say we no longer want the weight attribute
    products.remove( "products", "weight" );

    # Make the query
    results = products.get_products();
    print results

Pagination
~~~~~~~~~~

The Semantics3 API allows for pagination, so you can request for, say, 5
results, and then continue to obtain the next 5 from where you stopped
previously. For the python semantics3 module, we have implemented this
using iterators. All you have to do is specify a cache size, and use it
the same way you would any iterator:

::

    # Specify a cache size
    products.cache(5)

    # Iterate through the results
    for i in products.iter():
        print i

Our library will automatically request for results 5 products at a time.

Explore Price Histories
~~~~~~~~~~~~~~~~~~~~~~~

For this example, we are going to look at a particular product that is
sold by select merchants and has a price of >= USD 30 and seen after a
specific date (specified as a UNIX timestamp).

::

    # Build the query
    products.offers_field( "sem3_id", "4znupRCkN6w2Q4Ke4s6sUC");
    products.offers_field( "seller", ["LFleurs","Frys","Walmart"] );
    products.offers_field( "currency", "USD");
    products.offers_field( "price", "gte", 30);
    products.offers_field( "lastrecorded_at", "gte", 1348654600);



    # Make the query
    results = products.get_offers()

    # View the results of the query
    print results

Contributing
------------

Use GitHub's standard fork/commit/pull-request cycle. If you have any
questions, email support@semantics3.com.

Author
------

-  Shawn Tan shawn@semantics3.com

Copyright
---------

Copyright (c) 2013 Semantics3 Inc.

License
-------

::

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

