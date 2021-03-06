from stockupapi.models.product_company_part import ProductPart
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import OrderRec, OrderRecProduct, OrderRecPart, Company, Product, CompanyPart, Part
from rest_framework.decorators import action 
import os.path

class OrderRecViewSet(ViewSet):
    def list(self, request):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            order_recs = OrderRec.objects.filter(company=company).order_by('-date_generated')[1:]

            serializer = OrderRecSerializer(order_recs, many=True, context={'request': request})

            return Response(serializer.data)
        else:
            return Response({"reset": True})
    
    def retrieve(self, request, pk):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            order_rec = OrderRec.objects.get(pk=pk, company=company)

            serializer = OrderRecSerializer(order_rec, context={'request': request})

            return Response(serializer.data)
        else:
            return Response({"reset": True})

    def create(self, request):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)
            # Create new OrderRec and save
            order_rec = OrderRec()
            order_rec.company = company
            order_rec.sales_start_date = request.data["salesStartDate"]
            order_rec.sales_end_date = request.data["salesEndDate"]

            order_rec.save()

            # To store various usages of the same part
            company_parts_dict = {}
            # Create new OrderRecProduct and save
            for sale in request.data["sales"]:
                product = Product.objects.get(pk=sale["productId"])

                order_rec_product = OrderRecProduct()
                order_rec_product.order_rec = order_rec
                order_rec_product.product = product
                order_rec_product.amount_sold = int(sale["amountSold"])

                order_rec_product.save()

                # Get ProductParts for each product
                product_parts = ProductPart.objects.filter(product=product, deleted=False)

                # Multiply amount_used of each part by the amount sold of that product
                for product_part in product_parts:
                    part_used_for_product = product_part.amount_used * order_rec_product.amount_sold
                    # Check to see if this part from inventory is already represented in the list
                    if product_part.company_part.id in company_parts_dict:
                        # Add to the list for the inventory part
                        company_parts_dict[product_part.company_part.id]["company_part_used"].append(part_used_for_product)
                    else:
                        # Add a list for this inventory part and then add the part amount used
                        company_parts_dict[product_part.company_part.id] = {}
                        company_parts_dict[product_part.company_part.id]["product_part_id"] = product_part.id
                        company_parts_dict[product_part.company_part.id]["company_part_id"] = product_part.company_part.id
                        company_parts_dict[product_part.company_part.id]["company_part_used"] = []
                        company_parts_dict[product_part.company_part.id]["company_part_used"].append(part_used_for_product)
        
            # Sum any like ProductPart answers (if a part is used on more than one product, add the 2 separate results that were multiplied)
            for part in company_parts_dict.values():
                company_part = CompanyPart.objects.get(pk=part["company_part_id"])
                part["company_part_used"] = sum(part["company_part_used"])
                # Subtract sum from in_inventory
                remaining_inventory = company_part.in_inventory - part["company_part_used"]
                # Compare to min required
                part_order_rec = company_part.min_required - remaining_inventory
                # Save company_part with new inventory amount
                company_part.in_inventory = remaining_inventory
                company_part.save()
                # Create new OrderRecParts for each ProductPart and total_used
                order_rec_part = OrderRecPart()
                order_rec_part.order_rec = order_rec
                order_rec_part.product_part_id = part["product_part_id"]
                order_rec_part.part_amount_to_order = part_order_rec

                # Negative means the that amount in inventory is higher than required, so no order needed
                if part_order_rec <= 0:
                    order_rec_part.part_amount_to_order = 0
                    order_rec_part.date_ordered = '2000-01-01'
                    order_rec_part.date_received = '2000-01-01'

                order_rec_part.save()

            serializer = OrderRecSerializer(order_rec, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"reset": True})

    def update(self, request, pk):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            if "productId" in request.data[0]:
                for product in request.data:
                    order_rec_product = OrderRecProduct.objects.get(order_rec_id=pk, product_id=product["productId"])
                    
                    original_amount_sold = order_rec_product.amount_sold

                    order_rec_product.amount_sold = int(product["amountSold"])

                    order_rec_product.save()
                        
                    recent_rec = OrderRec.objects.filter(company=company).order_by('-date_generated')[0]

                    if recent_rec.id == int(pk):
                        product_parts = ProductPart.objects.filter(product_id=product["productId"], deleted=False)

                        for product_part in product_parts:
                            # Original part order recommendation 
                            company_part = CompanyPart.objects.get(productpart=product_part, productpart__product_id=product["productId"])
                            order_rec_part = OrderRecPart.objects.get(order_rec_id=pk, product_part__company_part_id=company_part.id)

                            new_part_used_for_product = product_part.amount_used * order_rec_product.amount_sold
                            original_part_used_for_product = product_part.amount_used * original_amount_sold

                            company_part.in_inventory = company_part.in_inventory + original_part_used_for_product - new_part_used_for_product
                            company_part.save()
                            
                            company_part_order_rec = company_part.min_required - company_part.in_inventory


                            # Negative means the that amount in inventory is higher than required, so no order needed
                            if company_part_order_rec <= 0:
                                order_rec_part.part_amount_to_order = 0
                                if order_rec_part.date_ordered == None:
                                    order_rec_part.date_ordered = '2000-01-01'
                                    order_rec_part.date_received = '2000-01-01'
                            else:
                                order_rec_part.part_amount_to_order = company_part_order_rec
                                # Prevents removal of good date if user changes sales after ordering
                                if str(order_rec_part.date_ordered) == '2000-01-01':
                                    order_rec_part.date_ordered = None
                                    order_rec_part.date_received = None
                            
                            order_rec_part.save()
            # TODO: Remove and return 204 when this works a few more times
            order_rec = OrderRec.objects.get(pk=pk)

            serializer = OrderRecSerializer(order_rec, context={'request': request})

            return Response(serializer.data)
        else:
            return Response({"reset": True})

    @action(methods=["get"], detail=False)
    def recent(self, request):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            try:
                order_rec = OrderRec.objects.filter(company=company).order_by('-date_generated')[0]

                serializer = OrderRecSerializer(order_rec, context={'request': request})
                
                return Response(serializer.data)
            except IndexError:
                return Response({'error': 'no order rec found'})
        else:
            return Response({"reset": True})
    
    @action(methods=["post"], detail=False)
    def change_status(self, request):
        if request.reset == False:
            company = Company.objects.get(employee__user = request.auth.user)

            order_rec_part = OrderRecPart.objects.get(pk=request.data["recPartId"])

            if len(request.data) == 3:
                order_rec_part.part_amount_ordered = request.data["amountOrdered"]
                order_rec_part.date_ordered = request.data["dateOrdered"]

            else:
                company_part = CompanyPart.objects.get(productpart__orderrecpart=order_rec_part)

                company_part.in_inventory += order_rec_part.part_amount_ordered

                company_part.save()

                order_rec_part.date_received = request.data["dateReceived"]

            order_rec_part.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"reset": True})

class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part

        fields = '__all__'
        depth=1

class CompanyPartSerializer(serializers.ModelSerializer):

    part = PartSerializer()

    class Meta:
        model = CompanyPart

        fields = '__all__'

class ProductPartSerializer(serializers.ModelSerializer):
    
    company_part = CompanyPartSerializer()

    class Meta:
        model = ProductPart

        fields = ("company_part",)

class OrderRecPartSerializer(serializers.ModelSerializer):

    product_part = ProductPartSerializer()

    class Meta:

        model = OrderRecPart

        exclude = ['order_rec']

class OrderRecProductSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        try:
            order_rec_id = os.path.split(self.context["request"].path)[1]

            order_rec_product = OrderRecProduct.objects.get(order_rec_id=order_rec_id, product_id=instance.id)

            return {
                "id": instance.id,
                "name": instance.name,
                "deleted": instance.deleted,
                "amount_sold": order_rec_product.amount_sold,
            }
           
        except:
            return {
                "id": instance.id,
                "name": instance.name,
                "deleted": instance.deleted,
            }

class ProductSerializer(OrderRecProductSerializer):
    
    class Meta:

        model = Product

        fields = (OrderRecProductSerializer(),)

class OrderRecSerializer(serializers.ModelSerializer):

    orderrecpart_set = OrderRecPartSerializer(many=True)
    products = ProductSerializer(many=True, context={'order_rec': OrderRec})

    class Meta:

        model = OrderRec

        fields = ('id', 'date_generated', 'sales_start_date', 'sales_end_date', 'products', 'orderrecpart_set')
