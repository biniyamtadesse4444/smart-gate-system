from datetime import date, timedelta
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from core.models import Customer

class Article(models.Model):
    id = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    duration = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['id']

class Payment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='payments')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='payments', null=True, blank=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    return_url = models.URLField(null=True, blank=True)
    getway_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    reminder_sent = models.BooleanField(default=False)



    def calculate_end_date(self):
        return self.start_date + timedelta(days=self.article.duration) 
    
    def calculate_puagume_date(self):
        return self.start_date + timedelta(days=self.article.duration + 5)
     
        

    def save(self, *args, **kwargs):
        if self.start_date and self.article:
            base_end_date = self.start_date + timedelta(days=self.article.duration)
            puagume_date = date(base_end_date.year, 9, 5)
            if base_end_date == puagume_date:
                self.end_date = self.start_date + timedelta(days=self.article.duration + 5)
            else:
                self.end_date = base_end_date

        super().save(*args, **kwargs)



#Username