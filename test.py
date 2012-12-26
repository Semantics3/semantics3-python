from semantics3 import semantics3 

#set up class structure
#interface with module and make simple request

api_key = 'INSERT_API_KEY'
api_secret = 'INSERT_API_SECRET'

c = semantics3.Products(api_key,api_secret)
d = c.test()
e = c.test()

#set up inheritance
#query product id
#scale up
