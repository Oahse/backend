from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.user_views import (
    CreateUserViewSet, LoginViewSet, TradepersonViewSet, BusinessViewSet,
    DistributorViewSet, DelivererViewSet, 
    VerifyEmailView, ResetPasswordRequestView, ProfessionViewSet
)

router = DefaultRouter()
router.register(r'clients', CreateUserViewSet, basename='user')
router.register(r'tradepersons', TradepersonViewSet, basename='tradeperson')
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'distributors', DistributorViewSet, basename='distributor')
router.register(r'deliverers', DelivererViewSet, basename='deliverer')
router.register(r'professions', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', LoginViewSet.as_view({'post': 'logout'}), name='logout'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', ResetPasswordRequestView.as_view(), name='password-reset-request')
]