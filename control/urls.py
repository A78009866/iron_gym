from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('approve/<int:sub_id>/', views.approve_subscription, name='approve_subscription'),
    path('user/<int:user_id>/', views.user_detail_view, name='user_detail'), # URL for user details
    path('renew/admin/<int:sub_id>/', views.renew_subscription_admin, name='renew_subscription_admin'), # URL for admin renewal
    path('renew/user/', views.renew_subscription_user, name='renew_subscription_user'), # URL for user renewal
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'), # New URL for deleting user
]