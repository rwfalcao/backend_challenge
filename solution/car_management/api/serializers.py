from rest_framework import serializers
from car_management.models import Car

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = [
            'current_gas_level', 
            'gas_capacity'
            ]

