from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.quotation_views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]