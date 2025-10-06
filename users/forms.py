from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'bio', 'avatar']
        labels = {
            'email': 'Email',
            'bio': 'О себе',
            'avatar': 'Аватар',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите немного о себе...'
            }),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
