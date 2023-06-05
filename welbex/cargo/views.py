from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


from .models import Shipment, Car
from .serializers import (
    ShipmentSerializer,
    ShipmentCarSerializer,
    CarSerializer,
    ShipmentDetailsSerializer,
    ShipmentCreateSerializer
)


class ShipmentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]


class ShipmentDetailsView(generics.RetrieveAPIView):
    queryset = Shipment.objects.select_related('pick_up')
    serializer_class = ShipmentDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        shipment = self.get_object()
        serializer = ShipmentDetailsSerializer(shipment)
        data = serializer.data

        numbers_with_distances = Car.objects.get_numbers_with_distances(
            shipment.pick_up.lat,
            shipment.pick_up.lon,
        )
        data['car_distances'] = numbers_with_distances
        return Response(data)


class ShipmentCreateView(generics.CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentCreateSerializer
    permission_classes = [IsAuthenticated]


class ShipmentListView(generics.ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentCarSerializer

    def list(self, request, *args, **kwargs):
        radius = request.GET.get('radius', settings.CARS_LOOKUP_RADIUS_MI)
        min_weight = request.GET.get('min_weight')
        max_weight = request.GET.get('max_weight')
        queryset = Shipment.objects.with_cars_nearby(
            radius,
            min_weight,
            max_weight
        )
        serializer = ShipmentCarSerializer(queryset, many=True)
        return Response(serializer.data)


class CarView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
