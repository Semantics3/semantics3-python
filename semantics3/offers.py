try:
    from .semantics3 import Semantics3Request
except ImportError:
    from semantics3 import Semantics3Request

class Offers(Semantics3Request):
    def __init__(self, api_key, api_secret, api_base='https://api.semantics3.com/v1/'):
        Semantics3Request.__init__(self, api_key, api_secret, 'offers', api_base)

    def get_offers(self):
        return self.get()

    def offers_field(self, *field):
        return self.field(*field)
