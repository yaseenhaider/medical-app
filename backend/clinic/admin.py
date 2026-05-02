from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'scheduled_at', 'status', 'created_at')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('patient__email', 'doctor__email', 'reason')
