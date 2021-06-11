from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from safedelete.config import DELETED_ONLY_VISIBLE, DELETED_VISIBLE, DELETED_VISIBLE_BY_FIELD
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from safedelete.managers import SafeDeleteManager

class MyModelManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_VISIBLE_BY_FIELD

class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = CharField(max_length=150)
    company = ForeignKey("Company", on_delete=CASCADE)
    image = ImageField(upload_to='products', height_field=None, width_field=None, max_length=None, null=True)
    parts = ManyToManyField("CompanyPart", through="ProductPart", related_name="product_part")