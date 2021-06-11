from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stockupapi.models import Vendor

class VendorViewSet(ViewSet):
    def list(self, request):
        vendors = Vendor.objects.all()

        serializer = VendorSerializer(vendors, many=True, context={'request': request})

        return Response(serializer.data)

class VendorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Vendor

        fields = '__all__'