from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            'username',
            'email'
        )

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.exclude(
                pk=self.instance.pk
        ).filter(
            email=email
        ).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

class ProfileForm(forms.ModelForm):

    class Meta:

        model = CustomerProfile

        fields = (
            'phone',
            'address',
            'profile_picture'
        )

        widgets = {

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'profile_picture': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
