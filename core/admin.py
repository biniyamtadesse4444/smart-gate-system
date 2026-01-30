from django import forms
from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth import get_user_model
from .models import Customer, Door, House, Reader, Card
from payment.models import Payment
from django.contrib.auth.admin import UserAdmin as BaseAdmin

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'card_status', 'card_type', 'remark', ]
    list_select_related = ['customer']
    list_filter = ['card_status', 'card_type']
    search_fields = ['id', 'customer__first_name', 'customer__last_name']
    list_per_page = 15
    autocomplete_fields = ['customer']

    
    def first_name(self, card: Card):
        return card.customer.first_name if card.customer else ''
    
    def last_name(self, card: Card):
        return card.customer.last_name if card.customer else ''


class CardInline(admin.TabularInline):
    model = Card
    min_num=0
    max_num=2
    extra=1

class PaymentInline(admin.TabularInline):
    model = Payment
    readonly_fields = ['end_date']
    exclude = ['return_url', 'getway_reference']
    autocomplete_fields = ['article']
    min_num = 0
    extra = 1

class HouseInline(admin.TabularInline):
    model = House
    readonly_fields = ['customer']
    min_num = 0
    max_num = 1
    extra = 1


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    
    inlines = [CardInline, PaymentInline, HouseInline]
    list_display_links = ['phone_number']
    list_display = ['phone_number', 'first_name', 'last_name', 'issued_date', 'is_active']
    list_filter = ['issued_date', 'is_active']
    search_fields = ['first_name', 'last_name', 'id']   
    list_per_page = 15
    search_fields = ['first_name', 'last_name']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "usable_password", "password1", "password2", 'first_name', 'last_name'),
            },
        ),
    )
   
   #username


# Register your models here.
