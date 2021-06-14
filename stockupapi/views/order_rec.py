from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import OrderRec, OrderRecProduct, OrderRecPart, Company, Product, CompanyPart
import os.path

class OrderRecViewSet(ViewSet):

    def create(self, request):
        company = Company.objects.get(employee__user = request.auth.user)
        # Create new OrderRec and save
        order_rec = OrderRec()
        order_rec.company = company

        order_rec.save()

        # To store various usages of the same part
        company_parts_dict = {}
        # Create new OrderRecProduct and save
        for sale in request.data["sales"]:
            product = Product.objects.get(pk=sale["productId"])

            order_rec_product = OrderRecProduct()
            order_rec_product.order_rec = order_rec
            order_rec_product.product = product
            order_rec_product.amount_sold = sale["amountSold"]

            order_rec_product.save()

            # Get ProductParts for each product
            product_parts = ProductPart.objects.filter(product=product)

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
            # Negative means the that amount in inventory is higher than required, so no order needed
            if part_order_rec < 0:
                part_order_rec = 0
            # Save company_part with new inventory amount
            company_part.in_inventory = remaining_inventory
            company_part.save()
            # Create new OrderRecParts for each ProductPart and total_used
            order_rec_part = OrderRecPart()
            order_rec_part.order_rec = order_rec
            order_rec_part.product_part_id = part["product_part_id"]
            order_rec_part.part_amount_to_order = part_order_rec

            order_rec_part.save()

        serializer = OrderRecSerializer(order_rec, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class OrderRecSerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderRec

        fields = '__all__'