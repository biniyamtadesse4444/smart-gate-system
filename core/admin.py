from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Customer, Door, House, Reader, Card
from payment.models import Payment

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'card_status', 'card_type', 'remark', ]
    list_select_related = ['customer']
    list_filter = ['card_status', 'card_type']
    search_fields = ['id', 'customer__first_name', 'customer__last_name']
    list_per_page = 15
    autocomplete_fields = ['customer']


    def first_name(self, card: Card):
        return card.customer.first_name
    
    def last_name(self, card: Card):
        return card.customer.last_name,


class CardInline(admin.TabularInline):
    model = Card
    min_num=1
    max_num=2
    extra=1

class PaymentInline(GenericTabularInline):
    model = Payment
    readonly_fields = ['end_date']
    autocomplete_fields = ['article']
    min_num = 1
    max_num = 1
    extra = 0
    

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [CardInline, PaymentInline]
    readonly_fields = ['user']
    list_display_links = ['phone_number']
    list_display = ['phone_number', 'first_name', 'last_name', 'issued_date', 'is_active', 'user']
    list_filter = ['issued_date', 'is_active']
    search_fields = ['first_name', 'last_name', 'id']   
    readonly_fields = ['user']
    list_per_page = 15
    search_fields = ['first_name', 'last_name']
    exclude = ['user']


# Register your models here.
