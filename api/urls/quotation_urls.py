from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.quotation_views import QuotationViewSet

router = DefaultRouter()
router.register(r'', QuotationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]