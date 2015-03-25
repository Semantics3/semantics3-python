try:
    from .semantics3 import Semantics3Request
except ImportError:
    from semantics3 import Semantics3Request


class Products(Semantics3Request):
    def __init__(self, api_key, api_secret, api_base='https://api.semantics3.com/v1/'):
        Semantics3Request.__init__(self, api_key, api_secret, 'products', api_base)

    def get_products(self):
        return self.get()

    def get_offers(self):
        return self.get('offers')

    def get_categories(self):
        return self.get('categories')

    def products_field(self, *field):
        return self.field(*field)

    def offers_field(self, *field):
        return self.add('offers', *field)

    def categories_field(self, *field):
        return self.add('categories', *field)

    def sitedetails(self, field_name, field_value1, *field_value2):
        self.field(
            "sitedetails",
            field_name,
            field_value1,
            *field_value2
        )

    def latestoffers(self, field_name, field_value1, field_value2):
        self.field(
            "sitedetails",
            "latestoffers",
            field_name,
            field_value1,
            *field_value2
        )
