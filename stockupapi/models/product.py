from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class Product(models.Model):
    name = CharField(max_length=150)
    company = ForeignKey("Company", on_delete=CASCADE)
    image = ImageField(upload_to='products', height_field=None, width_field=None, max_length=None, null=True)
    parts = ManyToManyField("CompanyPart", through="ProductPart", related_name="products")
    deleted = BooleanField(default=False)