try:
    from .semantics3 import Semantics3Request
except ImportError:
    from semantics3 import Semantics3Request

class Offers(Semantics3Request):
    def __init__(self, api_key, api_secret):
        Semantics3Request.__init__(self, api_key, api_secret, 'offers')

    def get_offers(self):
        return self.get()

    def offers_field(self, *field):
        return self.field(*field)
