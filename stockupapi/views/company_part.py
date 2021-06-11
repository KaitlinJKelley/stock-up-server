from .part import PartSerializer
from django.views.generic.base import View
from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, CompanyPart

class UserInventoryViewSet(ViewSet):
    def create(self, request):
        # TODO: Handle image upload
        company = Company.objects.get(employee__user = request.auth.user)

        part = Part.objects.get(pk=request.data["partId"])
        
        # Create a company_part (adds the part to the company's inventory)
        company_part = CompanyPart()
        company_part.company = company
        company_part.part = part
        company_part.in_inventory = request.data["inInventory"]
        company_part.min_required = request.data["minRequired"]
        company_part.cost = request.data["cost"]

        company_part.save()

        serializer = CompanyPartSerializer(company_part, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class CompanyPartSerializer(serializers.ModelSerializer):

    part = PartSerializer(many=False)

    class Meta:

        model = CompanyPart

        fields = '__all__'