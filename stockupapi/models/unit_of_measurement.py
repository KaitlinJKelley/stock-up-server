from django.db import models
from django.db.models.fields import CharField

class UnitOfMeasurement(models.Model):
    label = CharField(max_length=20)