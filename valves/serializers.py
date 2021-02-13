from collections import OrderedDict
from rest_framework import serializers

from .models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        # fields = ('code', 'dn', 'equip_type', 'full_title', 'kvs', 'price', 'type_title', 'z', 'discount_group')
        # fields = '__all__'
        exclude = ('id',)

    def to_representation(self, instance):
        result = super(EquipmentSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class EquipmentSerializerWithoutDiscountGroup(EquipmentSerializer):
    class Meta:
        model = Equipment
        exclude = ('id', 'discount_group')