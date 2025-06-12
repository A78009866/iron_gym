from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Subscription
from django.utils import timezone
from datetime import timedelta

# Add this helper function for superuser check
def is_superuser(user):
    return user.is_superuser

# الصفحة الرئيسية وتسجيل اشتراك جديد
def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        duration = request.POST.get('duration')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل.')
            return redirect('home')

        user = User.objects.create_user(username=username, password=password)
        
        Subscription.objects.create(
            user=user,
            requested_duration=int(duration)
        )
        
        # تسجيل دخول المستخدم مباشرة
        login(request, user)
        
        messages.success(request, 'تم إرسال طلب اشتراكك بنجاح. الرجاء انتظار موافقة المسؤول.')
        return redirect('dashboard')

    return render(request, 'home.html')

# صفحة تسجيل الدخول
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'بيانات الاعتماد غير صحيحة.')
            return redirect('login')
    return render(request, 'login.html')

# لوحة التحكم
@login_required
def dashboard_view(request):
    context = {}
    if request.user.is_superuser:
        pending_subscriptions = Subscription.objects.filter(is_active=False)
        active_subscriptions = Subscription.objects.filter(is_active=True).order_by('-end_date')
        context = {
            'pending_subscriptions': pending_subscriptions,
            'active_subscriptions': active_subscriptions,
        }
    else:
        try:
            subscription = Subscription.objects.get(user=request.user)
            context = {
                'subscription': subscription
            }
        except Subscription.DoesNotExist:
            context = {
                'subscription': None
            }
            # messages.info(request, "لا يوجد لديك اشتراك حالياً. يمكنك تقديم طلب اشتراك جديد.")
            # return redirect('home') # Removed redirect here to show message on dashboard
            
    return render(request, 'dashboard.html', context)

# الموافقة على الاشتراك (للمسؤول فقط)
@login_required
@user_passes_test(is_superuser)
def approve_subscription(request, sub_id):
    try:
        sub = Subscription.objects.get(id=sub_id)
        sub.is_active = True
        sub.end_date = timezone.now() + timedelta(days=sub.requested_duration)
        sub.save()
        messages.success(request, f"تم تفعيل اشتراك المستخدم {sub.user.username}.")
    except Subscription.DoesNotExist:
        messages.error(request, "الاشتراك غير موجود.")

    return redirect('dashboard')

# تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# User Detail View (New)
@login_required
@user_passes_test(is_superuser) # Only superusers can access this view
def user_detail_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    # Ensure superusers cannot view their own details through this admin view if it causes issues,
    # or handle gracefully. For simplicity, just allow if superuser.
    
    try:
        subscription = Subscription.objects.get(user=user_obj)
    except Subscription.DoesNotExist:
        subscription = None
    
    context = {
        'user_obj': user_obj,
        'subscription': subscription
    }
    return render(request, 'user_detail.html', context)

# Renew Subscription for Admin (New)
@login_required
@user_passes_test(is_superuser) # Only superusers can access this view
def renew_subscription_admin(request, sub_id):
    if request.method == 'POST':
        sub = get_object_or_404(Subscription, id=sub_id)
        duration_days = int(request.POST.get('duration')) # Duration from dropdown

        # If subscription is active and has remaining time, extend from current end_date, otherwise from now
        if sub.is_active and sub.end_date and sub.end_date > timezone.now():
            sub.end_date += timedelta(days=duration_days)
        else: # If expired, inactive, or never set
            sub.end_date = timezone.now() + timedelta(days=duration_days)
            sub.is_active = True # Ensure it's active

        sub.save()
        messages.success(request, f"تم تجديد اشتراك المستخدم {sub.user.username} لمدة {duration_days} يوم.")
    else:
        messages.error(request, "طلب تجديد غير صالح.")
    
    return redirect('user_detail', user_id=sub.user.id) # Redirect back to user detail page

# Renew Subscription for Regular User (New)
@login_required
def renew_subscription_user(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        messages.error(request, "لا يوجد اشتراك لتجديده.")
        return redirect('home')

    if request.method == 'POST':
        duration_days = int(request.POST.get('duration')) # Duration from dropdown

        # If subscription is active, extend from current end_date, otherwise from now
        if subscription.is_active and subscription.end_date and subscription.end_date > timezone.now():
            subscription.end_date += timedelta(days=duration_days)
        else:
            subscription.end_date = timezone.now() + timedelta(days=duration_days)
            subscription.is_active = True # Ensure it's active if it was expired/pending

        subscription.save()
        messages.success(request, f"تم تجديد اشتراكك بنجاح لمدة {duration_days} يوم.")
    else:
        messages.error(request, "طلب تجديد غير صالح.")
    
    return redirect('dashboard')

# New: Delete User View
@login_required
@user_passes_test(is_superuser) # Only superusers can delete users
def delete_user_view(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    # Prevent a superuser from deleting themselves (optional but recommended)
    if request.user.id == user_to_delete.id:
        messages.error(request, "لا يمكنك حذف حسابك الخاص كمسؤول.")
        return redirect('user_detail', user_id=user_id)

    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, f"تم حذف المستخدم '{user_to_delete.username}' بنجاح.")
        return redirect('dashboard') # Redirect to dashboard after deletion
    
    # If not a POST request, just redirect or show an error
    messages.error(request, "طلب غير صالح لحذف المستخدم.")
    return redirect('user_detail', user_id=user_id)