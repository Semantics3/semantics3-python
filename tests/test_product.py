from semantics3 import Products
import unittest
from os import environ

sem3 = Products(
        api_key = environ["SEM3_API_KEY"],
        api_secret = environ["SEM3_API_SECRET"]
        )


class TestProductAPI(unittest.TestCase):

    """Docstring for TestProductAPI. """
    def test_get_products(self):
        """@todo: Docstring for test_get_products.
        :returns: @todo

        """
        sem3.products_field("search", "iphone")
        results = sem3.get_products()
        self.assertEqual(results['code'], 'OK')
        sem3.clear_query()

    def test_upc_query(self):
        """@todo: Docstring for test_upc_query.
        :returns: @todo

        """
        pass
        sem3.products_field("upc", "883974958450")
        sem3.products_field("field", ["name","gtins"])
        results = sem3.get_products()
        self.assertEqual(results['code'], 'OK')
        sem3.clear_query()

    def test_url_query(self):
        """@todo: Docstring for test_url_query.
        :returns: @todo

        """
        sem3.products_field("url", "http://www.walmart.com/ip/15833173")
        results = sem3.get_products()
        self.assertEqual(results['code'], 'OK')
        sem3.clear_query()
    
    def test_price_query(self):
        """@todo: Docstring for test_price_query.
        :returns: @todo

        """
        sem3.products_field("search", "iphone")
        sem3.products_field("price", "lt", 300)
        results = sem3.get_products()
        self.assertEqual(results['code'], 'OK')
        sem3.clear_query()

    def test_catid_query(self):
        """@todo: Docstring for test_catid_query.
        :returns: @todo

        """
        sem3.categories_field("cat_id", 4992)
        results = sem3.get_categories()
        self.assertEqual(results['code'], 'OK')
        sem3.clear_query()
