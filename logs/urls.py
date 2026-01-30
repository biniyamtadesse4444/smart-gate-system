from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = routers.DefaultRouter()
router.register(r'cards', views.AccessLogViewSet, basename='card')
router.register(r'attendance', views.AttendanceViewSet)


urlpatterns = router.urls 

