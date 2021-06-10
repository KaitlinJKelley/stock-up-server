import json
from stockupapi.models.unit_of_measurement import UnitOfMeasurement
from stockupapi.models.vendor import Vendor
from django.views.generic.base import View
from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError, ViewDoesNotExist
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models.company_parts import CompanyPart
from stockupapi.models import Company
# from .company_part import CompanyPartSerializer

class PartDatabaseViewSet(ViewSet):
    def list(self, request):
        all_parts = Part.objects.all()

        serializer = PartSerializer(all_parts, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        # TODO: Handle image upload
        uom = UnitOfMeasurement.objects.get(pk=request.data["unitOfMeasurement"])

        new_part = Part()
        new_part.name = request.data["name"]
        new_part.part_number = request.data["partNumber"]
        new_part.unit_of_measurement = uom

        if type(request.data["vendor"]) == int:
            vendor = Vendor.objects.get(pk=request.data["vendor"])
            new_part.vendor = vendor

            new_part.save()
        elif type(request.data["vendor"]) == str:
            new_vendor = Vendor()
            new_vendor.name = request.data["vendor"]
            new_vendor.website = request.data["website"]

            new_vendor.save()

            new_part.vendor = new_vendor

            new_part.save()

        serializer = PartSerializer(new_part, many=False, context={'request': request})

        company = Company.objects.get(employee__user = request.auth.user)
        

        company_part = CompanyPart()
        company_part.company = company
        company_part.part = new_part
        company_part.in_inventory = request.data["inInventory"]
        company_part.min_required = request.data["minRequired"]
        company_part.cost = request.data["cost"]
        

        company_part.save()

        # How to add an additional field to serializer.data, such as message that part was also added to user inventory
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Part

        fields = '__all__'
        depth = 1
class PartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Part

        fields = '__all__'

