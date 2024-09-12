# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.transaction_views import DeliveryTrackerViewSet

router = DefaultRouter()
router.register(r'', DeliveryTrackerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]