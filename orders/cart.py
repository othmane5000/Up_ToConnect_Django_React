from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        # Sécurité : on vérifie que le produit existe vraiment et qu'il est actif
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return False

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity}

        # Sécurité : on ne dépasse jamais le stock disponible
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock

        self.save()
        return True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return

        if quantity <= 0:
            self.remove(product_id)
            return

        # Sécurité : jamais plus que le stock réel
        quantity = min(quantity, product.stock)
        self.cart[product_id] = {'quantity': quantity}
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        # Sécurité : le prix vient TOUJOURS de la base de données, jamais de la session
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        products_map = {str(p.id): p for p in products}

        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            yield {
                'product': product,
                'quantity': item['quantity'],
                'unit_price': product.price,
                'subtotal': product.price * item['quantity'],
            }

    def get_total(self):
        return sum(item['subtotal'] for item in self)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())