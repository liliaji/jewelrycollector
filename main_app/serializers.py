from rest_framework import serializers
from .models import Jewelry, Feeding

class JewelrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Jewelry
        fields = '__all__'

class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'
        read_only_fields = ('jewelry',)

