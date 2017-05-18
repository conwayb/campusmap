from rest_framework import serializers

from .models import BicycleParking, BicycleRoute


class BicycleParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BicycleParking
        fields = '__all__'


class BicycleRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BicycleRoute
        fields = '__all__'
