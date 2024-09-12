from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.quotation_views import CartViewSet

router = DefaultRouter()
router.register(r'', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]