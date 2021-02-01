from collections import OrderedDict
from rest_framework import serializers

from .models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

    def to_representation(self, instance):
        result = super(EquipmentSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
