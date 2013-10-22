__all__ = ['categories', 'offers', 'products', 'semantics3', 'error']

try:
    from .semantics3 import Semantics3Request
    from .categories import Categories
    from .offers import Offers
    from .products import Products
except ImportError:
    from semantics3 import Semantics3Request
    from categories import Categories
    from offers import Offers
    from products import Products
