from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Location, Shipment, Car


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ['zip', 'city', 'state', 'lat', 'lon']
        read_only_fields = ['zip', 'city', 'state', 'lat', 'lon']


class ShipmentSerializer(ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'pick_up', 'delivery', 'weight', 'description']
        read_only_fields = ['id', 'pick_up', 'delivery']


class ShipmentCreateSerializer(ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'pick_up', 'delivery', 'weight', 'description']


class ShipmentDetailsSerializer(ModelSerializer):
    pick_up = LocationSerializer()
    delivery = LocationSerializer()

    class Meta:
        model = Shipment
        fields = ['id', 'pick_up', 'delivery', 'weight', 'description']


class ShipmentCarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pick_up = serializers.PrimaryKeyRelatedField(read_only=True)
    delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    weight = serializers.IntegerField()
    description = serializers.CharField()
    cars_nearby = serializers.IntegerField()


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'number', 'location', 'carrying']
        read_only_fields = ['id', 'number', 'carrying']
