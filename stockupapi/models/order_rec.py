from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField, DateField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class OrderRec(models.Model):
    date_generated = DateTimeField(auto_now_add=True)
    sales_start_date = DateField(default=None, null=True)
    sales_end_date = DateField(default=None, null=True)
    company = ForeignKey("Company", on_delete=CASCADE)
    products = ManyToManyField("Product", through="OrderRecProduct", related_name='order_recs')
    parts = ManyToManyField("ProductPart", through="OrderRecPart")
    
    