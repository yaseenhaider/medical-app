from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import MedicalUser


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=MedicalUser.Role.choices)

    class Meta(UserCreationForm.Meta):
        model = MedicalUser
        fields = ('first_name', 'last_name', 'email', 'role')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if MedicalUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
