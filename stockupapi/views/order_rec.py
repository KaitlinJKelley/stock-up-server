from stockupapi.models.product_company_part import ProductPart
from stockupapi.models.parts import Part
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import OrderRec, OrderRecProduct, OrderRecPart, Company, Product
import os.path

class OrderRecViewSet(ViewSet):
    # {
    #     "sales": [
    #         {
    #             "productId": 1,
    #             "amountSold": 3
    #         },
    #         {
    #             "productId": 2,
    #             "amountSold": 4
    #         }
    #     ]
    # }

    def create(self, request):
        company = Company.objects.get(employee__user = request.auth.user)
        # Create new OrderRec and save
        order_rec = OrderRec()
        order_rec.company = company

        # order_rec.save()

        product_parts_list = []
        company_part_occurrences = []
        # Create new OrderRecProduct and save
        for sale in request.data["sales"]:
            product = Product.objects.get(pk=sale["productId"])

            order_rec_product = OrderRecProduct()
            order_rec_product.order_rec = order_rec
            order_rec_product.product = product
            order_rec_product.amount_sold = sale["amountSold"]

            # order_rec_product.save()

            # Get ProductParts for each product
            product_parts = ProductPart.objects.filter(product=product)

            # Multiply amount_used of each part by the amount sold of that product
            for product_part in product_parts:
                amount_used = product_part.amount_used * order_rec_product.amount_sold
                product_part.amount_used = amount_used

                product_parts_list.append(product_part)
                company_part_occurrences.append(product_part.company_part.id)

        # Sum any like ProductPart answers (if a part is used on more than one product, add the 2 separate results that were multiplied)
        # TODO: Consider changing relationship on ERD to use company_part id instead of product_company_part
        # TODO: Consider combining product_parts_list and company_part_occurrences to:
            # {
                # company_part id : [amount, amount, amount], 
                # company_part id : [amount, amount, amount] 
            # }
        # Create new OrderRecParts for each ProductPart and total_used