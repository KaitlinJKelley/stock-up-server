from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey

class Company(models.Model):
    class report_view_choices(models.TextChoices):
        weekly = 'weekly'
        monthly = 'monthly'
        quarterly = 'quarterly'
        yearly = 'yearly'
    
    class order_schedule_choices(models.TextChoices):
        weekly = 'weekly'
        biweekly = 'biweekly'
        monthly = 'monthly'
        bimonthly = 'bimonthly'
        quarterly = 'quarterly'

    company_name = CharField(max_length=200)
    ein = CharField(max_length=25)
    report_view = CharField(choices=report_view_choices.choices, null=True, max_length=100)
    order_schedule = CharField(choices=order_schedule_choices.choices, null=True, max_length=100)
    cat_pref = ForeignKey("Category", null=True, on_delete=SET_NULL)
    logo  = ImageField(upload_to='logos', height_field=None, width_field=None, max_length=None, null=True, blank=True)

    