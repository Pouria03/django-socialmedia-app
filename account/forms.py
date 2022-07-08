from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# this form is for user registration
class RegisterUserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exist = User.objects.filter(email=email).exists()
        if user_exist:
            raise ValidationError('this email is taken')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user_exist = User.objects.filter(username=username).exists()
        if user_exist:
            raise ValidationError('this username is taken')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2:
            raise ValidationError('passwords must match')


#  login form

class LoginForm(forms.Form):
    email = forms.CharField(label='username or email')
    password = forms.CharField(widget=forms.PasswordInput())

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('this email doesn\'t exist')
        return email

class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)