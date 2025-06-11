from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Subscriber
from django.contrib.auth.decorators import login_required

@login_required
def subscriber_list(request):
    # This is the corrected view. The loop has been removed.
    active_subscribers = Subscriber.objects.filter(end_date__gte=timezone.now().date())
    context = {'subscribers': active_subscribers}
    return render(request, 'subscriber_list.html', context)

@login_required
def add_subscriber(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = int(request.POST.get('duration'))
        
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=duration)
        
        Subscriber.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('subscriber_list')
        
    return render(request, 'add_subscriber.html')

@login_required
def expired_list(request):
    expired_subscribers = Subscriber.objects.filter(end_date__lt=timezone.now().date())
    context = {'subscribers': expired_subscribers}
    return render(request, 'expired_list.html', context)

@login_required
def renew_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    subscriber.start_date = timezone.now().date()
    subscriber.end_date = subscriber.start_date + timedelta(days=30)
    subscriber.save()
    return redirect('subscriber_list')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Subscriber

@require_POST
def delete_subscriber(request, pk):
    try:
        subscriber = Subscriber.objects.get(id=pk)
        subscriber.delete()
        return JsonResponse({'success': True})
    except Subscriber.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'المشترك غير موجود'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

