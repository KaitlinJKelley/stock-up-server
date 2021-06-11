from django.db import models
from stockupapi.models.product import Product
from stockupapi.models.company_parts import CompanyPart
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField, BooleanField
from django.db.models.fields.related import ForeignKey

class ProductPart(models.Model):
    deleted = BooleanField(default=False)
    product = ForeignKey(Product, on_delete=CASCADE)
    company_part = ForeignKey(CompanyPart, on_delete=CASCADE)
    amount_used = IntegerField()

    @staticmethod
    def soft_delete(self, product_part):
        product_part.deleted=True
        product_part.save()

