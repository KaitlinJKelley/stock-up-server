from django.db import models
from django.db.models.fields import CharField

class Category(models.Model):
    label = CharField(max_length=25)