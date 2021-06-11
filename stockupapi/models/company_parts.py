from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import DecimalField, IntegerField, FloatField
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

    @property
    def round(self):
        self.cost = round(self.cost, 2)

    # TODO: Consider moving image field here so user's can upload the image of their part
