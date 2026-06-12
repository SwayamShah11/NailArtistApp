from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'service',
        'appointment_date',
        'appointment_time',
        'status'
    )

    list_filter = (
        'status',
        'appointment_date'
    )
