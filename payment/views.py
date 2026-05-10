from datetime import date, datetime, timedelta
from decimal import Decimal
import json
from uuid import uuid4
from django.conf import settings
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from core.models import Customer
from payment.models import Article, Payment
from payment.serializers import ChappaVaildPayment, CreatePaymentSerializer, CustomerSerializer, FailedPaymentSerializer, PostPaymentSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from payment.validators import validate_payment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils import timezone

tx_ref = None

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.prefetch_related("cards", 'payments').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_object_or_404(
            Customer,
            phone_number=request.user.pk
        )
        if request.method == 'GET':
            
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['post']

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_object_or_404(
            Customer,
            phone_number=request.user.pk
        )
        
        serializer = CreatePaymentSerializer(customer)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.user.phone_number
        article_id = serializer.validated_data['article_id']


        result = validate_payment(customer_id, article_id)

        if result['status'] == 'failed':
            data1 = {
                'status': 'failed',
                'reason': result.get('reason', 'Unknown error')
            }
            serializer = FailedPaymentSerializer(data=data1)
            serializer.is_valid(raise_exception=True)
            # serializer.save()

            return Response(
                serializer.data, 
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        elif(result['status'] == 'success'):
            
            
            url = "https://api.chapa.co/v1/transaction/initialize"
            tx_ref = f"order-{uuid4().hex[:10]}"

            payload = {
                "amount": str(result['amount']),
                "currency": 'ETB',
                "phone_number": result['phone_number'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "tx_ref": tx_ref,
                "callback_url": "https://postsigmoidal-dorsiferous-nyla.ngrok-free.dev/sunshine/chapa/callback/",
                "return_url": 'http://127.0.0.1:8000/sunshine/pay/',
                "meta": {
                    "disable_phone_edit": False,
                    "article_id": result['article'].id,
                    "customer_phone": result['customer'].phone_number,
                    "start_date": str(result['n_start_date']),
                    "end_date": str(result['n_end_date']), 
                }
            }

            headers = {
                'Authorization': f'Bearer CHASECK_TEST-EoslYwwIKeZ9e1fGfZgXWg0ZJAeHiEb7',
                'Content-Type': 'application/json'
                }
        
            response = requests.post(url, json=payload, headers=headers)
            
            data = response.json()
            

            if data.get('status') == 'success':

                return Response({'checkout_url': data['data']['checkout_url'], 'tx_ref': tx_ref},
                            status=status.HTTP_200_OK)
            else:
                return Response({'error': data}, status=status.HTTP_400_BAD_REQUEST)

           


@csrf_exempt
@api_view(["POST", "GET"])
def chapa_callback(request):
    
    tx_ref = request.data.get("tx_ref") or request.GET.get("trx_ref")

    if not tx_ref:
        return Response({"error": "Missing tx_ref"}, status=400)
    
    else:
        verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }
        get_payload = ''

        get_response = requests.get(verify_url, headers=headers, data=get_payload)      

    try:
        response = requests.get(verify_url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return Response({"error": "Verification failed"}, status=502)

    if data.get("status") != "success":
        return Response({"status": "verification failed"}, status=400)

    verified = data["data"]

    if Payment.objects.filter(getway_reference=tx_ref).exists():
        return Response({"status": "already processed"}, status=200)

    meta = verified.get("meta", {})

    try:
        customer = Customer.objects.get(
            phone_number=meta.get("customer_phone")
        )
        article = Article.objects.get(pk=meta.get("article_id"))
    except (Customer.DoesNotExist, Article.DoesNotExist):
        return Response({"error": "Invalid metadata"}, status=400)
    

    payment_data = {
        "customer": customer.phone_number,
        "article": article.id,
        "start_date": date.fromisoformat(meta.get("start_date")),
        "end_date": date.fromisoformat(meta.get("end_date")),
        "tx_ref": tx_ref,
        "getway_reference": verified.get("reference"),
    }
    print(payment_data['end_date'])

    payment_serializer = ChappaVaildPayment(data=payment_data)
    payment_serializer.is_valid(raise_exception=True)
    payment_serializer.save()
    
    return Response({"status": "payment saved"}, status=200)   





# @csrf_exempt
# @api_view(['POST'])

# def chappa_callback(request):
#     tx_ref = request.data.get("tx_ref") or request.data.get("tx_ref")
    
#     if not tx_ref:
#         return Response({"error": "Missing tx_ref in payload"}, status=400)

#     verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
#     headers = {
#         "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
#     }

#     try:
#         response = requests.get(verify_url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         return Response({"error": "Verification failed"}, status=502)

#     # 4. Check Status and Update DB
#     if data.get("status") == "success" and data.get("data", {}).get("status") == "success":
#         if Payment.objects.filter(trx_ref=tx_ref).exists():
#             return Response({"status": "already saved"}, status=200)

#         meta = data["data"].get("meta", {})
        
#         try:
#             customer = Customer.objects.get(phone_number=meta.get("customer_phone"))
#             article = Article.objects.get(pk=meta.get("article_id"))
            
#             Payment.objects.create(
#                 customer=customer,
#                 article=article,
#                 start_date=meta.get("start_date"),
#                 end_date=meta.get("end_date"),
#                 trx_ref=tx_ref,
#                 getway_reference=data["data"]["reference"],
#             )
#             return Response({"status": "payment saved"}, status=200)
#         except (Customer.DoesNotExist, Article.DoesNotExist):
#             return Response({"error": "Invalid metadata references"}, status=400)

#     return Response({"status": "verification failed"}, status=400)
    # payment_data = {
    #         "article": article.id,
    #         "customer": customer.phone_number,
    #         "start_date": meta["start_date"],
    #         "end_date": meta["end_date"],
    #         "tx_ref": verified_data["tx_ref"],
    #         "getway_reference": verified_data["reference"],
    #         }

        
    #     if Payment.objects.filter(tx_ref=verified_data["tx_ref"]).exists():
    #         return JsonResponse({"status": "already processed"}, status=200)                
    #     payment_serializer = ChappaVaildPayment(data=payment_data)
    #     payment_serializer.is_valid(raise_exception=True)
    #     payment_serializer.save()     

    #     return JsonResponse({"status": "success"}, status=200)
    
                
            
    #JsonResponse


        


