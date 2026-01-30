from rest_framework import serializers
from django.utils import timezone
from core.models import Card, Customer
from payment.models import Payment
from math import ceil

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_type', 'card_status']
    
class PaymentInfoSerializer(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['start_date', 'end_date', 'remaining_days']

    def get_remaining_days(self, payment):
        today = timezone.now().date()
        remaining_days = (payment.end_date - today).days
        if remaining_days < 0:
            month = ceil(abs(remaining_days / 30))
            return f'To make your card active you must pay {month} Month package(s)'
        return remaining_days
    
    

class CustomerSerializer(serializers.ModelSerializer):
    cards = CardSerializer(read_only=True, many=True)
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['phone_number', 'first_name', 'last_name', 'cards', 'payment']

    def get_payment(self, customer):

        payment = customer.payments.order_by('-end_date').first()

        if not payment:
            return None

        return PaymentInfoSerializer(payment).data


class CreatePaymentSerializer(serializers.Serializer):
    article_id = serializers.CharField()

class FailedPaymentSerializer(serializers.Serializer):
    status = serializers.CharField()
    reason = serializers.CharField()

class ChappaVaildPayment(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['article', 'start_date', 'end_date', 'customer', 'getway_reference']

class PostPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    currency = serializers.CharField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    tx_ref = serializers.CharField()
    callback_url = serializers.CharField()
    return_url = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    duration = serializers.IntegerField()
    