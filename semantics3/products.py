from semantics3 import Semantics3Request

class Products(Semantics3Request):
	def __init__(self, api_key, api_secret):
		Semantics3Request.__init__(self, api_key, api_secret, 'products')

	def get_products(self):
		return self.get()
	
	def products_field(self, *field):
		return self.field(*field)

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

