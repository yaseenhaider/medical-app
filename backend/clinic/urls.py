from django.urls import path

from .views import AppointmentListView

app_name = 'clinic'

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
]
