"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls.about_urls')),
    path('api/products/', include('api.urls.product_urls')),
    path('api/users/', include('api.urls.user_urls')), 
    path('api/address/', include('api.urls.address_urls')),
    path('api/quotations/', include('api.urls.quotation_urls')),
    path('api/categories/', include('api.urls.category_urls')),
    path('api/orders/', include('api.urls.order_urls')),
    path('api/carts/', include('api.urls.cart_urls')),
    path('api/transactions/', include('api.urls.transaction_urls')),
    path('api/deliverytrackers/', include('api.urls.deliverytracker_urls')),
    path('api/messages/', include('api.urls.messages_urls')),
    path('api/jobs/', include('api.urls.jobs_urls')),
    path('api/services/', include('api.urls.service_urls')),
    path('api/reviews/', include('api.urls.reviews_urls')),
    path('api/comments/', include('api.urls.comments_urls')),
    # path('api/notifications/', include('api.urls.notification_urls')),
    # path('api/reports/', include('api.urls.report_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)