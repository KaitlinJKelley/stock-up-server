from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import Company, Product, CompanyPart
import os.path

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
    
    def retrieve(self, request, pk):
        company = Company.objects.get(employee__user = request.auth.user)

        try:
            product = Product.objects.get(pk=pk, company=company)

            serializer = ProductSerializer(product, many=False, context={'request': request})

            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response({"error": "This product does not exist or you may not have access to view it"})



class PartSerializer(serializers.ModelSerializer):

    class Meta:
      
        model = Part

        fields = ('name',) 

# Custom serializer
class ProductPartSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        # instance = CompanyPart object
        id = instance.id
        
        # splits the request path to retrieve the id of the product 
        product = os.path.split(self.context["request"].path)[1]
        product_part = ProductPart.objects.get(company_part=id, product__id=product)
        instance.amount_used = product_part.amount_used

        return {
            "id": instance.id,
            "name": PartSerializer(instance.part).data["name"],
            "amount_used": instance.amount_used
        }

class CompanyPartSerializer(ProductPartSerializer):

    # Passes the Product object to the ProductPartSerializer
    part = ProductPartSerializer(many=False, context={"product": Product})

    class Meta:
      
        model = CompanyPart

        fields = ('id','name','part',)

class ProductSerializer(serializers.ModelSerializer):

    parts = CompanyPartSerializer(many=True)

    class Meta:
        model = Product

        fields = ('id', 'name', 'parts')

    