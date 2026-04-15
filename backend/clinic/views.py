from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Appointment


class AppointmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'clinic/appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role == user.Role.DOCTOR:
            queryset = Appointment.objects.select_related('patient', 'doctor').filter(doctor=user)
        else:
            queryset = Appointment.objects.select_related('patient', 'doctor').filter(patient=user)
        context['appointments'] = queryset.order_by('-scheduled_at')
        context['now'] = timezone.now()
        return context
