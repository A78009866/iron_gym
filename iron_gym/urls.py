from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # استخدام المسار 'login/' لتسجيل الدخول
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # استخدام المسار 'logout/' لتسجيل الخروج
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # تضمين روابط تطبيق members
    path('', include('control.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)