from stockupapi.models.product import Product
from stockupapi.models.order_rec import OrderRec
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey

class OrderRecProduct(models.Model):
    order_rec = ForeignKey(OrderRec, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    amount_sold = IntegerField(null=False)