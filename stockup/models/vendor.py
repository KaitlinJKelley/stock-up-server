from django.db import models
from django.db.models.fields import CharField, URLField

class Vendor(models.Model):
    name = CharField(max_length=100)
    website = URLField()