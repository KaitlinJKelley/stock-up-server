from stockupapi.models.product import Product
from stockupapi.models.company_parts import CompanyPart
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from safedelete.config import DELETED_ONLY_VISIBLE, DELETED_VISIBLE, DELETED_VISIBLE_BY_FIELD
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from safedelete.managers import SafeDeleteManager, SafeDeleteDeletedManager

class ProductPart(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    objects = SafeDeleteManager()
    deleted_objects = SafeDeleteDeletedManager()
    product = ForeignKey(Product, on_delete=CASCADE)
    company_part = ForeignKey(CompanyPart, on_delete=CASCADE)
    amount_used = IntegerField()