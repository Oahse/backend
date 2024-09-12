# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.job_views import ServiceViewSet

router = DefaultRouter()
router.register(r'', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]