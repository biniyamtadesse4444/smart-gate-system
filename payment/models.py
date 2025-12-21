from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

class Payment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='payments')
    start_date = models.DateField()
    end_date = models.DateField()
    object_id = models.CharField(max_length=11)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def calculate_end_date(self):
        return self.start_date + timedelta(days=self.article.duration) 