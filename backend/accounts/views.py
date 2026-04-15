from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from clinic.models import Appointment

from .forms import LoginForm, SignupForm
from .models import MedicalUser


class HomeView(TemplateView):
    template_name = 'accounts/home.html'


class UserSignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/redirect.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        role = request.user.role
        if role == MedicalUser.Role.DOCTOR:
            return redirect('accounts:doctor_dashboard')
        if role == MedicalUser.Role.ADMIN:
            return redirect('accounts:admin_dashboard')
        return redirect('accounts:patient_dashboard')


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/patient_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = (
            Appointment.objects.select_related('doctor')
            .filter(patient=self.request.user)
            .order_by('-scheduled_at')[:10]
        )
        return context


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/doctor_dashboard.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.role != MedicalUser.Role.DOCTOR:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = (
            Appointment.objects.select_related('patient')
            .filter(doctor=self.request.user)
            .order_by('scheduled_at')[:10]
        )
        return context


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/admin_dashboard.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.role != MedicalUser.Role.ADMIN:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_by_role'] = (
            MedicalUser.objects.values('role')
            .annotate(total=Count('id'))
            .order_by('role')
        )
        context['appointment_count'] = Appointment.objects.count()
        return context
