from django.db import models
from django.db.models.deletion import DO_NOTHING, SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class CompanyVendor(models.Model):

    company = ForeignKey("Company", on_delete=DO_NOTHING)
    vendor = ForeignKey("Vendor", on_delete=DO_NOTHING)
    sales_rep_name = CharField(max_length=100, null=True)
    sales_rep_phone = CharField(max_length=40, null=True)
    address = CharField(max_length=200, null=True)
    login_username = CharField(max_length=100, null=True)
    login_password = CharField(max_length=100, null=True)