from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.quotation_views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
