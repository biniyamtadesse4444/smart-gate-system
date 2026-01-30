from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from core.models import Reader
from logs.models import AccessLog
from logs.serializers import  AttendanceSerializer, PostCardInfoSerializer, GetCardInfoSerializer
from core.validators import validate_card
from rest_framework.response import Response
from rest_framework import status


class AccessLogViewSet(ModelViewSet):
    queryset = AccessLog.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = PostCardInfoSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCardInfoSerializer
        return GetCardInfoSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = PostCardInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        card_id = validated_data['card_id']
        reader_id = validated_data['reader_id']
        
    
        result = validate_card(card_id, reader_id)

        log_data = {
            'access_time': result['time'],
            'card' : result['card'],
            'customer': result['customer'],
            'event': result['event'],
            'reader': result['reader'],
            'access_granted': result['granted'],
            'door': result['door']
        }

        if result['granted'] == True:
            log_serializer = GetCardInfoSerializer(data=log_data)
            log_serializer.is_valid(raise_exception=True)
            log_serializer.save()
            return Response(
            {
            'access_time': result['time'],
            'customer': result['customer'],
            "card": result["card"],
            'access_granted': result['granted'],
            "event": result["event"],
            'door': result['door'], 
            'status': result['status']       
             
            }, status=status.HTTP_200_OK,
            )


        
        
        return Response(
            {
            'access_time': result['time'],
            'customer': result['customer'],
            "card": result["card"],
            'access_granted': result['granted'],
            "event": result["event"],
            'door': result['door'], 
            'status': result['status']       
             
            }, status=status.HTTP_200_OK,
            )
    

class AttendanceViewSet(ModelViewSet):
    queryset = AccessLog.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCardInfoSerializer
        return AttendanceSerializer
    
    
    def create(self, request, *args, **kwargs):
        serialzer = PostCardInfoSerializer(data=request.data)
        serialzer.is_valid(raise_exception=True)

        validated_data = serialzer.validated_data

        card_id = validated_data['card_id']
        reader_id = validated_data['reader_id']

        result = validate_card(card_id, reader_id)

        if result['granted'] == True:

            attendance_data = {
                'access_time': result['time'],
                'card' : result['card'],
                'customer': result['customer'],
                'event': result['event'],
                'reader': result['reader'],
                'access_granted': result['granted'],
                'door': result['door']
            }

            attendance_serializer = AttendanceSerializer(data = attendance_data)
            attendance_serializer.is_valid(raise_exception=True)
            attendance_serializer.save()
            return Response(
            {
            'access_time': result['time'],
            'customer': result['customer'],
            "card": result["card"],
            'access_granted': result['granted'],
            "event": result["event"],
            'door': result['door'], 
            'status': result['status']       
             
            }, status=status.HTTP_200_OK,
            )
        return None