from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='arabic_date')
def arabic_date(value):
    """
    فلتر لتحويل تاريخ ميلادي إلى شكل عربي.
    مثال: 11 يونيو 2025
    """
    if not value:
        return ""

    # التأكد من أن القيمة هي كائن تاريخ
    if isinstance(value, str):
        # محاولة تحويل النص إلى تاريخ (افترض الصيغة YYYY-MM-DD)
        try:
            value = timezone.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return value

    arabic_months = [
        "جانفي", "فيفري", "مارس", "أفريل", "ماي", "جوان",
        "جويلية", "اوت", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
    ]

    day = value.day
    month_name = arabic_months[value.month - 1]
    year = value.year

    return f"{day} {month_name} {year}"