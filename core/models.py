from django.conf import settings
from django.db import models
from django.contrib import admin


class Customer(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True, editable=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    issued_date = models.DateField(auto_now_add=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, editable=False,related_name='customer')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # sync phone_number to User.username
        if self.user.username != self.phone_number:
            self.user.username = self.phone_number
            self.user.save(update_fields=['username'])
    
    class Meta:
        ordering = ['first_name', 'last_name']

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

    id = models.CharField(max_length=7, primary_key=True)
    card_type = models.CharField(max_length=1, choices=CARD_TYPE_CHOICE, default=C_MEMBER)
    card_model = models.CharField(max_length=1, choices=CARD_MODEL_CHOICE, default=C_STICKER)
    card_status = models.CharField(max_length=1, choices=CARD_STATUS_CHOICE, default=C_ACTIVE)
    registered_date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cards')

    def __str__(self) -> str:
        return str(self.id)
    
    @admin.display(ordering='customer__first_name')
    def first_name(self):
        return self.customer.first_name
    
    @admin.display(ordering='customer__last_name')
    def last_name(self):
        return self.customer.last_name
    
    def is_valid(self) -> bool:
        return (self.card_status == self.C_ACTIVE and
                self.customer.is_active
                )
    
    def can_open(self, door: 'Door') -> bool:
        if not door.is_active:
            return False
        if self.card_type == self.C_MASTER:
            return self.is_valid()
        
        return(
            self.is_valid() and 
            self.door_permissions.filter(
                door = door,
                can_access=True
            ).exists()
        )

    
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

    def allowed_card(self):
        return Card.objects.filter(
            door_permissions=self,
            door_permissions__can_access=True,
            card_status=Card.C_ACTIVE,
            customer__is_active=True
        )
    
    def __str__(self) -> str:
        return self.door

class DoorPermission(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='doorpermissions')
    door = models.ForeignKey(Door, on_delete=models.CASCADE, related_name='doorpermissions')
    can_access = models.BooleanField(default=True)

    class Meta:
        unique_together = ['card', 'door']

class Reader(models.Model):
    name = models.CharField(max_length=50)
    door = models.ForeignKey(Door, on_delete=models.CASCADE, related_name='readers')

    def __str__(self):
        return self.name

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
# Create your models here.
