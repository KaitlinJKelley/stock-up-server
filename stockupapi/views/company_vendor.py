from stockupapi.models.company_vendor import CompanyVendor
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stockupapi.models import Vendor, Company

class CompanyVendorViewSet(ViewSet):
    def list(self, request):
        company = Company.objects.get(employee__user = request.auth.user)

        company_vendors = CompanyVendor.objects.filter(company=company)

        serializer = CompanyVendorSerializer(company_vendors, many=True, context={"request": request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        company = Company.objects.get(employee__user = request.auth.user)

        company_vendor = CompanyVendor.objects.get(pk=pk, company=company)

        serializer = CompanyVendorSerializer(company_vendor, context={'request': request})

        return Response(serializer.data)

class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Vendor

        fields = '__all__'

class CompanyVendorSerializer(serializers.ModelSerializer):

    vendor = VendorSerializer()

    class Meta:

        model = CompanyVendor

        fields = '__all__'