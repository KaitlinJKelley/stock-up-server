from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, Product, CompanyPart
from stockupapi.views.company_part import CompanyInventoryViewSet

class ProductViewSet(ViewSet):

    def list(self, request):
        company = Company.objects.get(employee__user = request.auth.user)

        products = Product.objects.filter(company=company)

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data["id"], serializer.data["name"])
    
    def create(self, request):
        # TODO: Add image handling

        company = Company.objects.get(employee__user = request.auth.user)

        product = Product()
        product.company = company
        product.name = request.data["name"]

        product.save()

        for part in request.data["parts"]:
            company_part = CompanyPart.objects.get(pk=part["partId"])
            
            product_part = ProductPart()

            product_part.product = product
            product_part.company_part = company_part
            product_part.amount_used = part["amountUsed"]

            product_part.save()

        serializer = ProductSerializer(product, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductSerializer(serializers.ModelSerializer):

    # def part_partial_serialize(self, obj):
    #     part = CompanyInventoryViewSet.CompanyPartSerializer(obj, many=True)

    #     return part

    # parts = serializers.SerializerMethodField(method_name = "part_partial_serialize")

    # parts = CompanyInventoryViewSet.CompanyPartSerializer(many=True)

    class Meta:
        model = Product

        fields = ('id', 'name', 'parts')
        depth = 1

    