from rest_framework import serializers

from .models import BicycleParking


class BicycleParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BicycleParking
        fields = '__all__'
