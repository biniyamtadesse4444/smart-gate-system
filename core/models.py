from django.conf import settings
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'A'
    CUSTOMER = 'C'
    CATEGORY_CHOICE = [
        (ADMIN, "ADMIN"),
        (CUSTOMER, "CUSTOMER"),
    ]

    phone_number = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICE, default=CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    issued_date = models.DateField(auto_now_add=True, editable=False)
    email = models.EmailField(null=True, blank=True, max_length=255, unique=True)

    objects = CustomerManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]


class Card(models.Model):
    #card type choices
    C_MASTER = 'M'
    C_MEMBER = 'm'
    #card model choices
    C_KEY_CHAIN = 'K'
    C_STICKER = 'S'
    C_WRIST_BAND = 'W'
    #card status choices 
    C_ACTIVE = 'A'
    C_INACTIVE = 'I'
    C_LOST = 'L'

    CARD_TYPE_CHOICE = [(C_MASTER, 'MASTER'),  (C_MEMBER, 'MEMBER')]

    CARD_MODEL_CHOICE = [
        (C_KEY_CHAIN, 'KEY CHAIN'),
        (C_STICKER, 'STICKER'),
        (C_WRIST_BAND, 'WRIST BAND')
    ]

    CARD_STATUS_CHOICE = [
        (C_ACTIVE, 'ACTIVE'),
        (C_INACTIVE, 'IN ACTIVE'),
        (C_LOST, 'LOST')
    ]

    id = models.CharField(max_length=9, primary_key=True)
    pin = models.CharField(max_length=4, default="0000")
    
    card_type = models.CharField(max_length=1, choices=CARD_TYPE_CHOICE, default=C_MEMBER)
    card_model = models.CharField(max_length=1, choices=CARD_MODEL_CHOICE, default=C_STICKER)
    card_status = models.CharField(max_length=1, choices=CARD_STATUS_CHOICE, default=C_ACTIVE)
    registered_date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=250, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    index = models.PositiveBigIntegerField(null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    @admin.display(ordering='customer__first_name')
    def first_name(self):
        return self.customer.first_name
    
    @admin.display(ordering='customer__last_name')
    def last_name(self):
        return self.customer.last_name
        
    
    class Meta:
        ordering = ['customer__first_name', 'customer__last_name']
   

class Door(models.Model):

    ENTRANCE = 'I'
    EXIT = 'O'

    DOOR_TYPE = [
        (ENTRANCE, 'ENTRANCE'),
        (EXIT, 'EXIT')
    ]

    door = models.CharField(max_length=1, choices=DOOR_TYPE)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        id = self.id
        return str(id)

class DoorPermission(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='doorpermissions')
    door = models.ForeignKey(Door, on_delete=models.CASCADE, related_name='doorpermissions')
    can_access = models.BooleanField(default=False)

    class Meta:
        unique_together = ['card', 'door']
        indexes = [
            models.Index(fields=['can_access']),
        ]

class Reader(models.Model):
    name = models.CharField(max_length=50)
    door = models.ForeignKey(Door, on_delete=models.CASCADE, related_name='readers')
    api_key = models.CharField(max_length=64, unique=True, null=True, blank=True,)
    def __str__(self):
        id = self.id
        return str(id)

class House(models.Model):
    VILLA = 'V'
    APPARTMENT = 'A'
    HOUSE_TYPE_CHOICE = [
        (VILLA, 'VILLA'),
        (APPARTMENT, 'APPARTMENT')
    ]
    
    house_type = models.CharField(max_length=1, choices=HOUSE_TYPE_CHOICE)
    block = models.PositiveIntegerField()
    floor = models.PositiveIntegerField(null=True, blank=True)
    house_no = models.CharField(max_length=3)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='houses')

    class Meta:
        ordering = ['house_type', 'block', 'floor', 'house_no']

