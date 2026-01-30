from rest_framework import serializers
from core.models import Card, Customer

class GetCardSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()

    class Meta:
        model = Card
        fields = ['id', 'card_type', 'card_status', 'card_model', 'customer']

class PutCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id']

