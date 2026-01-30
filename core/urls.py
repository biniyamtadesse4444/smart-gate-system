from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='card')


urlpatterns = router.urls 

