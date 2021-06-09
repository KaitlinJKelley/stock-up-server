from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey

class OrderRec(models.Model):
    date_generated = DateTimeField(auto_now_add=True)
    company = ForeignKey("Company", on_delete=CASCADE)