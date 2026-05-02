from django.test import TestCase
from django.urls import reverse

from .models import MedicalUser


class AuthFlowTests(TestCase):
    def test_signup_creates_real_user_record(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'first_name': 'Ali',
                'last_name': 'Khan',
                'email': 'ali@example.com',
                'role': MedicalUser.Role.PATIENT,
                'password1': 'StrongPass123$',
                'password2': 'StrongPass123$',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MedicalUser.objects.filter(email='ali@example.com').exists())

    def test_role_based_dashboard_redirect(self):
        doctor = MedicalUser.objects.create_user(
            username='doc@example.com',
            email='doc@example.com',
            password='StrongPass123$',
            role=MedicalUser.Role.DOCTOR,
        )
        self.client.login(username='doc@example.com', password='StrongPass123$')
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertRedirects(response, reverse('accounts:doctor_dashboard'))
