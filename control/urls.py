# members/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.subscriber_list, name='subscriber_list'),
    path('add/', views.add_subscriber, name='add_subscriber'),
    path('expired/', views.expired_list, name='expired_list'),
    path('renew/<int:pk>/', views.renew_subscriber, name='renew_subscriber'),
    path('delete/<int:pk>/', views.delete_subscriber, name='delete_subscriber'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)