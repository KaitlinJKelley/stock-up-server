from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = CharField(max_length=150)
    company = ForeignKey("Company", on_delete=CASCADE)
    image = ImageField(upload_to='products', height_field=None, width_field=None, max_length=None, null=True)