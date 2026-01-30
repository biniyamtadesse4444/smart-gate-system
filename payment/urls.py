from . import views
from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import chapa_callback

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customers')
router.register(r'pay', views.PaymentViewSet, basename='payments')

urlpatterns = [
    path("chapa/callback/", chapa_callback, name="chapa-callback"),
]
urlpatterns += router.urls