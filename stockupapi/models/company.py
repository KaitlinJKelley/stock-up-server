from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class Company(models.Model):

    company_name = CharField(max_length=200)
    ein = CharField(max_length=25)
    report_view = CharField(null=True, max_length=100)
    order_schedule = CharField(null=True, max_length=100)
    cat_pref = ForeignKey("Category", null=True, on_delete=SET_NULL)
    logo  = ImageField(upload_to='logos', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    parts = ManyToManyField("Part", through="CompanyPart", related_name="companies")
    vendor = ManyToManyField("Vendor", related_name="companies")

    