from stockupapi.models.company_parts import CompanyPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, Product

class ProductViewSet(ViewSet):

    def list(self, request):
        company = Company.objects.get(employee__user = request.auth.user)

        products = Product.objects.filter(company=company)

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data["id"], serializer.data["name"])

class ProductSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Product

            fields = ('id', 'name', 'parts')

    