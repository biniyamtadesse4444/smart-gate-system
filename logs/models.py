from django.db import models
from core.models import Card, Door, Reader


class AccessLog(models.Model):
    access_time = models.DateTimeField(auto_now_add=True)
    card = models.CharField(max_length=20)
    customer = models.CharField(max_length=150, null=True, blank=True)
    reader = models.ForeignKey(Reader, on_delete=models.SET_NULL, null=True, related_name='access_logs')
    event = models.CharField(max_length=30, blank=True,null=True)
    access_granted = models.BooleanField(default=False)
    door = models.ForeignKey(Door, on_delete=models.SET_NULL, null=True, related_name='access_logs')
    
    class Meta:
        ordering = ['-access_time']
        indexes = [
            models.Index(fields=['access_time']),
            models.Index(fields=['access_granted']),
            models.Index(fields=['door', 'access_time']),
            models.Index(fields=['card', 'access_time']),
        ]

    def __str__(self):
        status = "GRANTED" if self.access_granted else "DENIED"
        return f"{self.card} → {self.door} ({status})"

class Attendance(models.Model):
    access_time = models.DateTimeField(auto_now_add=True)
    card = models.CharField(max_length=20)
    customer = models.CharField(max_length=150, null=True, blank=True)
    reader = models.ForeignKey(Reader, on_delete=models.SET_NULL, null=True, related_name='attendance')
    event = models.CharField(max_length=30, blank=True,null=True)
    access_granted = models.BooleanField(default=False)
    door = models.ForeignKey(Door, on_delete=models.SET_NULL, null=True, related_name='attendance')
    
    
