from django.views.generic.base import View
from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, Product, CompanyPart

class PartDatabaseViewSet(ViewSet):
    class PartSerializer(serializers.ModelSerializer):

        class Meta:

            model = Part

            fields = '__all__'