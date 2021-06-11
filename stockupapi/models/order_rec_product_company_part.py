from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField, DateField
from django.db.models.fields.related import ForeignKey

class OrderRecPart(models.Model):
    order_rec = ForeignKey("OrderRec", on_delete=CASCADE)
    product_part = ForeignKey("ProductPart", on_delete=CASCADE)
    part_amount_to_order = IntegerField(null=False)
    part_amount_ordered = IntegerField(null=True)
    date_ordered = DateField(null=True)
    received_date = DateField(null=True)
    