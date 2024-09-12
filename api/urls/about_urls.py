from django.urls import path
from ..views.about_views import HomeView, AboutAPIView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutAPIView.as_view(), name='about'),
]