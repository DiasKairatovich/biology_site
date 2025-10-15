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
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        label="Роль",
        required=False,  # если не выбрали, будет default='student'
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        role = self.cleaned_data.get("role")
        if role:
            user.role = role
        if commit:
            user.save()
        return user
