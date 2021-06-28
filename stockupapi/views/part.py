from stockupapi.models.unit_of_measurement import UnitOfMeasurement
from stockupapi.models.vendor import Vendor
from stockupapi.models.parts import Part
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stockupapi.models import CompanyPart
from stockupapi.models import Company
from rest_framework.decorators import action

class PartDatabaseViewSet(ViewSet):
    def list(self, request):
        company = Company.objects.get(employee__user = request.auth.user)

        # Should return all parts EXCEPT the parts that have been added to the company's inventory AND are not marked deleted
        all_parts = Part.objects.all().exclude(companies=company, companypart__deleted=False)           

        serializer = PartSerializer(all_parts, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        # TODO: Handle image upload
        # Add the new part to the Part Databas (all parts added by any user)
        new_part = Part()
        new_part.name = request.data["name"]
        new_part.part_number = request.data["partNumber"]
        # If the client sends an integer it should be a vendor Id
        try: 
            vendor = Vendor.objects.get(pk=request.data["vendor"])
            new_part.vendor = vendor

        # If the client sends a string it should be a new vendor name and include a website url
        except ValueError: 
            new_vendor = Vendor()
            new_vendor.name = request.data["vendor"].title()
            new_vendor.website = request.data["vendorWebsite"]
            new_vendor.save()

            new_part.vendor = new_vendor
        
        try:
            uom = UnitOfMeasurement.objects.get(pk=request.data["unitOfMeasurement"])

            new_part.unit_of_measurement = uom
        except ValueError:
            new_uom = UnitOfMeasurement()
            new_uom.label = request.data["unitOfMeasurement"]
            new_uom.save()

            new_part.unit_of_measurement = new_uom

        new_part.save()

        serializer = PartSerializer(new_part, many=False, context={'request': request})
        # Get the company that the user creating the part belongs to
        company = Company.objects.get(employee__user = request.auth.user)
        
        # Create a company_part (adds the part to the company's inventory)
        company_part = CompanyPart()
        company_part.company = company
        company_part.part = new_part
        company_part.in_inventory = request.data["inInventory"]
        company_part.min_required = request.data["minRequired"]
        company_part.cost = request.data["cost"]
        

        company_part.save()

        #TODO: How to add an additional field to serializer.data, such as message that part was also added to user inventory
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def check_part(self, request):
        
        try:
            vendor = Vendor.objects.get(pk=request.data["vendor"])
            Part.objects.get(vendor=vendor, name=request.data["name"].title(), part_number=request.data["partNumber"])

            return Response({"exists": True})

        except Part.DoesNotExist:
            return Response({"exists": False})
        
        except ValueError:
            return Response({"exists": False})



class PartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Part

        fields = '__all__'
        depth = 1

