from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MedicalUser


@admin.register(MedicalUser)
class MedicalUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Medical App', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Medical App', {'fields': ('role', 'phone_number')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
