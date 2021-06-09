from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User

class Employee(models.Model):
    employee_id = IntegerField(null=True)
    company = ForeignKey("Company", on_delete=CASCADE)
    user = OneToOneField(User, on_delete=DO_NOTHING)