from .part import PartSerializer
from stockupapi.models.parts import Part
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
    
    def retrieve(self, request, pk):
        company = Company.objects.get(employee__user = request.auth.user)

        try:
            company_part = CompanyPart.objects.get(pk=pk, company=company) 

            serializer = CompanyPartSerializer(company_part, context={'request': request}) 

            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        except CompanyPart.DoesNotExist:
            return Response({"error": "You do not have permission to view this part, or the part may not exist"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request):
        company = Company.objects.get(employee__user = request.auth.user)

        company_parts = CompanyPart.objects.filter(company=company, deleted=False)

        serializer = CompanyPartSerializer(company_parts, many=True, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk):
        company = Company.objects.get(employee__user = request.auth.user)

        company_part = CompanyPart.objects.get(pk=pk, company=company)

        company_part.in_inventory = request.data["inInventory"]
        company_part.min_required = request.data["minRequired"]
        company_part.cost = request.data["cost"]

        company_part.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

class CompanyPartSerializer(serializers.ModelSerializer):

    part = PartSerializer(many=False)

    class Meta:

        model = CompanyPart

        fields = '__all__'
    