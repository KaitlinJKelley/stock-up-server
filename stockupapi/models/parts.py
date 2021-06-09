from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import DO_NOTHING, SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import ImageField

class Part(models.Model):
    name = CharField(max_length=100)
    unit_of_measurement = ForeignKey("UnitOfMeasurement", on_delete=DO_NOTHING)
    part_number = CharField(max_length=50) 
    vendor = ForeignKey("Vendor", on_delete=DO_NOTHING)
    category = ForeignKey("Category", on_delete=SET_NULL, null=True)
    image = ImageField(upload_to='parts', height_field=None, width_field=None, max_length=None, null=True)

    UniqueConstraint(fields=[name, part_number, vendor], name="unique_part")