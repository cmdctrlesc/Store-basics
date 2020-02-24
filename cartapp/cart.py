from decimal import Decimal
from django.conf import settings
from mainapp.models import Record


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, record, quantity=1, update_quantity=False):
        record_id = str(record.id)
        if record_id not in self.cart:
            self.cart[record_id] = {'quantity': 0, 'price': str(record.price)}
        if update_quantity:
            self.cart[record_id]['quantity'] = quantity
        else:
            self.cart[record_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, record):
        record_id = str(record.id)
        if record_id in self.cart:
            del self.cart[record_id]
            self.save()

    def __iter__(self):
        record_ids = self.cart.keys()
        records = Record.objects.filter(id__in=record_ids)
        for record in records:
            self.cart[str(record.id)]['record'] = record

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
