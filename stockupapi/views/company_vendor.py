from stockupapi.models import company_vendor
from stockupapi.models.company_vendor import CompanyVendor
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
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

    def update(self, request, pk):
        company = Company.objects.get(employee__user = request.auth.user)

        company_vendor = CompanyVendor.objects.get(pk=pk, company=company)

        company_vendor.sales_rep_name = request.data["salesRepName"]
        company_vendor.sales_rep_phone = request.data["salesRepPhone"]
        company_vendor.address = request.data["address"]
        company_vendor.login_username = request.data["loginUsername"]
        company_vendor.login_password = request.data["loginPassword"]

        company_vendor.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Vendor

        fields = '__all__'

class CompanyVendorSerializer(serializers.ModelSerializer):

    vendor = VendorSerializer()

    class Meta:

        model = CompanyVendor

        fields = '__all__'