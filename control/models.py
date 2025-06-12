from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requested_duration = models.IntegerField(default=30) # المدة المطلوبة بالأيام
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Subscription"

    @property
    def remaining_days(self):
        if self.is_active and self.end_date:
            remaining = self.end_date - timezone.now()
            # إرجاع 0 إذا كانت المدة قد انتهت
            return max(0, remaining.days)
        return None