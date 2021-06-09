from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class ProductPart(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    product = ForeignKey("Product", on_delete=CASCADE)
    company_part = ForeignKey("CompanyPart", on_delete=CASCADE)
    amount_used = IntegerField()