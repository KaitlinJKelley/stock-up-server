from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField, URLField

class Vendor(models.Model):
    name = CharField(max_length=100)
    website = URLField(null=False)

    class Meta:
        constraints = [UniqueConstraint(fields=['name', 'website'], name="unique_vendor")]