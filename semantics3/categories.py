from semantics3 import Semantics3Request
class Offers(Semantics3Request):
	def __init__(self, api_key, api_secret):
		Semantics3Request.__init__(self, api_key, api_secret, 'categories')
	def get_categories(self):
		return self.get()
	def categories_field(self, *field):
		return self.field(*field)
