from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المشترك")
    start_date = models.DateField(verbose_name="تاريخ بدء الاشتراك")
    end_date = models.DateField(verbose_name="تاريخ انتهاء الاشتراك")

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        """
        خاصية للتحقق مما إذا كان الاشتراك لا يزال ساريًا
        """
        return timezone.now().date() <= self.end_date

    @property
    def elapsed_days(self):
        """
        خاصية لحساب عدد الأيام التي مرت منذ بدء الاشتراك
        """
        if timezone.now().date() >= self.start_date:
            return (timezone.now().date() - self.start_date).days
        return 0