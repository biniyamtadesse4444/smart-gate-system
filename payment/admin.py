from django.contrib import admin
from django.utils import timezone
from core.models import Customer
from payment.models import Article, Payment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit_price', 'duration']
    ordering = ['unit_price']
    search_fields = ['name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','start_date', 'end_date', 'customer_name', 'article', 'customer__phone_number', 'remaining_day']
    readonly_fields = ['end_date']
    autocomplete_fields = ['article', 'customer']
    exclude = ['return_url', 'getway_reference']
    list_select_related = ['customer']
    list_filter = ['customer']
    search_fields = ['id', 'customer__first_name', 'customer__last_name', 'customer__phone_number']
    list_per_page = 15

    @admin.display(description="Customer Name")
    def customer_name(self, payment: Payment):
        if payment.customer:
            return f'{payment.customer.first_name} {payment.customer.last_name}'
        return "-"
    
    @admin.display(description='remaining day')
    def remaining_day(self, payment: Payment):
        if payment:
            remaining_day = payment.end_date - timezone.now().date()
            return remaining_day
    
    
    

#username

# Register your models here.
