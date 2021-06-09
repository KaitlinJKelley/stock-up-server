from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey

class OrderRecProducts(models.Model):
    order_rec = ForeignKey("OrderRec", on_delete=CASCADE)
    product = ForeignKey("Product", on_delete=CASCADE)
    amount_sold = IntegerField(null=False)