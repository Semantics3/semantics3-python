try:
    from .semantics3 import Semantics3Request
except ImportError:
    from semantics3 import Semantics3Request

class Categories(Semantics3Request):
    def __init__(self, api_key, api_secret, api_base='https://api.semantics3.com/v1/'):
        Semantics3Request.__init__(self, api_key, api_secret, 'categories', api_base)

    def get_categories(self):
        return self.get()

    def categories_field(self, *field):
        return self.field(*field)
