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
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            products = Product.objects.filter(company=company, deleted=False)

            serializer = ProductSerializer(products, many=True, context={'request': request})

            return Response(serializer.data)
        else:
            return Response({"reset": True})
    
    def create(self, request):
        # TODO: Add image handling
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)
            try:
                product = Product.objects.get(company=company, name=request.data["name"])
                product.deleted=False
            except Product.DoesNotExist:
                product = Product()
                product.company = company
                product.name = request.data["name"]

            product.save()
            # Create a ProductPart instance for every part the user added when they created the product
            for part in request.data["parts"]:
                company_part = CompanyPart.objects.get(pk=part["partId"])

                try:
                    # if this company_part has been on this product before
                    product_part = ProductPart.objects.get(company_part=company_part, product=product)

                    product_part.deleted = False

                    product_part.amount_used = part["amountUsed"]
                    
                except ProductPart.DoesNotExist:
                    # The company_part has never been added to this product
                    product_part = ProductPart()
                    product_part.product = product
                    product_part.company_part = company_part
                    product_part.amount_used = part["amountUsed"]

                product_part.save()

            serializer = ProductSerializer(product, many=False, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"reset": True})
    
    def retrieve(self, request, pk):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            try:
                product = Product.objects.get(pk=pk, company=company, deleted=False)

                serializer = ProductSerializer(product, many=False, context={'request': request})

                # Removes empty string where deleted part existed
                try:
                    while "" in serializer.data["parts"]:
                        serializer.data["parts"].remove("")
                except ValueError:
                    pass

                return Response(serializer.data)

            except Product.DoesNotExist:
                return Response({"error": "This product does not exist or you may not have access to view it"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"reset": True})

    def destroy(self, request, pk):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            try:
                product = Product.objects.get(pk=pk, company=company)

                # soft delete
                product.deleted = True
                
                product.save()

                # TODO: Consider deleting associated ProductParts

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Product.DoesNotExist:
                return Response({"error": "You do not have permission to delete this product"}, status=status.HTTP_401_UNAUTHORIZED)  
        else:
            return Response({"reset": True})

    def update(self, request, pk):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            try:
                product = Product.objects.get(pk=pk, company=company)
                product.name = request.data["name"]

                product.save()

                # Get all ProductPart objects associated with this product
                product_parts_to_soft_delete = ProductPart.objects.filter(product=product)

                # Soft delete all ProductPart objects
                for product_part in product_parts_to_soft_delete:
                    ProductPart.soft_delete(self, product_part)

                # Iterate over all company_part IDs passed from client
                for part in request.data["parts"]:
                    company_part = CompanyPart.objects.get(pk=part["partId"])
                
                    try:
                        # if this company_part has been on this product before
                        product_part = ProductPart.objects.get(company_part=company_part, product=product)

                        product_part.deleted = False

                        product_part.amount_used = part["amountUsed"]
                    
                    except ProductPart.DoesNotExist:
                        # The company_part has never been added to this product
                        product_part = ProductPart()
                        product_part.product = product
                        product_part.company_part = company_part
                        product_part.amount_used = part["amountUsed"]

                    product_part.save()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Product.DoesNotExist:
                return Response()
        else:
            return Response({"reset": True})

class PartSerializer(serializers.ModelSerializer):

    class Meta:
      
        model = Part

        fields = ('name', 'unit_of_measurement')
        depth=1 

# Custom serializer
class ProductPartSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        # instance = CompanyPart object
        id = instance.id
        
        try:
            # splits the request path to retrieve the id of the product
            product = os.path.split(self.context["request"].path)[1]
            product_part = ProductPart.objects.get(company_part=id, product__id=product, deleted=False)
            instance.amount_used = product_part.amount_used

            return {
                "id": instance.id,
                "name": PartSerializer(instance.part).data["name"],
                "unit_of_measurement": PartSerializer(instance.part).data["unit_of_measurement"],
                "amount_used": instance.amount_used
            }
        # try till not find a matching ProductPart for company_parts that have been deleted from this product
        except ProductPart.DoesNotExist:
            return ""
        except ValueError:
            # For GET and POST requests (no pk at the end of these requests)
            return {
                "id": instance.id,
                "name": PartSerializer(instance.part).data["name"]
            }

class CompanyPartSerializer(ProductPartSerializer):

    # Passes the Product object to the ProductPartSerializer
    part = ProductPartSerializer(many=False, context={"product": Product})

    class Meta:
      
        model = CompanyPart

        fields = ('id','name','part',)

class ProductSerializer(serializers.ModelSerializer):
    # Will try to serialize all parts on a product, including deleted parts
    parts = CompanyPartSerializer(many=True)

    class Meta:
        model = Product

        fields = ('id', 'name', 'parts', 'deleted')

    