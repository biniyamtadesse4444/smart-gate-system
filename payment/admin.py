from django.contrib import admin

from payment.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit_price', 'duration']
    ordering = ['unit_price']
    search_fields = ['name']



# Register your models here.
