from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, Product, CompanyPart, company_parts

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
        # Create a ProductPart instance for every part the user added when they created the product
        # TODO: Add products.part_list and append product_part as created; see what that does 
        for part in request.data["parts"]:
            company_part = CompanyPart.objects.get(pk=part["partId"])
            
            product_part = ProductPart()

            product_part.product = product
            product_part.company_part = company_part
            product_part.amount_used = part["amountUsed"]

            product_part.save()

        serializer = ProductSerializer(product, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PartSerializer(serializers.ModelSerializer):

    class Meta:
      
        model = Part

        fields = ('name',)   

class CompanyPartSerializer(serializers.ModelSerializer):

    part = PartSerializer(many=True)

    class Meta:
      
        model = CompanyPart

        fields = ('id', 'part')

class ProductSerializer(serializers.ModelSerializer):
    # TODO: pull specific data from CompanyPartSerializer, instead of send everything back
    
    parts = CompanyPartSerializer(many=True)

    class Meta:
        model = Product

        fields = ('id', 'name', 'parts')

    