from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from core.models import Card, Customer
from core.serializers import GetCardSerializer, PutCardSerializer

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = PutCardSerializer
    http_method_names = ['get']


    