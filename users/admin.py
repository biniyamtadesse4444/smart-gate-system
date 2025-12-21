from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.admin import CustomerAdmin
from core.models import Customer
from payment.models import Payment
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("phone_number",)
    list_display = ("phone_number", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "password1", "password2"),
        }),
    )

    search_fields = ("phone_number",)



