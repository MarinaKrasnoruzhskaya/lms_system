from django.contrib import admin

from users.models import User, Payments

admin.site.register(User)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
    )
