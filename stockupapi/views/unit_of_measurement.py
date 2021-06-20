from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stockupapi.models import UnitOfMeasurement
from rest_framework import status

class UnitOfMeasurementViewSet(ViewSet):
    def list(self, request):
        unit_of_measurement = UnitOfMeasurement.objects.all()

        serializer = UOMSerializer(unit_of_measurement, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        uom = UnitOfMeasurement()
        uom.label = request.data["label"]

        uom.save()

        serializer = UOMSerializer(uom, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UOMSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnitOfMeasurement

        fields = '__all__'