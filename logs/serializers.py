from rest_framework import serializers
from core.models import Card, Door, Reader
from .models import AccessLog

class PostCardInfoSerializer(serializers.ModelSerializer):
    reader_id = serializers.IntegerField()
    card_id = serializers.CharField()
    class Meta:
        model= AccessLog
        fields=['card_id', 'reader_id']

        def validate_reader_id(self, reader_id):
            if not Reader.objects.filter(pk=reader_id).exists():
                raise serializers.ValidationError('reader doesnt exist')
            return reader_id
        def validate_card_id(self, card_id):
            if not Card.objects.filter(pk=card_id):
                raise serializers.ValidationError('card does not exist')
            return card_id
  
    

class GetCardInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessLog
        fields = ['access_time', 'card', 'customer', 'reader','event']
    read_only = ['access_time', 'card', 'customer', 'reader','event']

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessLog
        fields = []