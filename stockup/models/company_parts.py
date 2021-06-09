from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import IntegerField, FloatField
from django.db.models.fields.related import ForeignKey
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class CompanyPart(SafeDeleteModel):
    _safedelete_policy=SOFT_DELETE
    company = ForeignKey("Company", on_delete=CASCADE)
    part = ForeignKey("Part", on_delete=DO_NOTHING)
    in_inventory = IntegerField()
    min_required = IntegerField()
    cost = FloatField()