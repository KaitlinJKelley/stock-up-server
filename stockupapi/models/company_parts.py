from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import BooleanField, IntegerField, FloatField
from django.db.models.fields.related import ForeignKey

class CompanyPart(models.Model):
    deleted = BooleanField(default=False)
    company = ForeignKey("Company", on_delete=CASCADE)
    part = ForeignKey("Part", on_delete=DO_NOTHING)
    in_inventory = IntegerField()
    min_required = IntegerField()
    cost = FloatField()