from django.http import HttpResponse as http
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
# Create your views here.
# a class to sign uer up (some validations are coded in forms.py):
class RegisterUser(View):
    template_name = 'account/register.html'
    form_class = RegisterUserForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'your account created successfully ,now login', 'success')
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


# a class to log user in (some validations are coded in forms.py) :
class LoginUserView(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request,'you logged in successfully','success')
                return redirect('posts:home')
            else:
                messages.warning(request,'username or password is incorrect','warning')
        return render(request, self.template_name,{'form':form})


# a class to log user out  ::
class UserLogOutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out','success')
        return redirect('account:register')

# when user has forgotten his password and enters his email for validation
# (some validations are coded in forms.py):
class ForgotPasswordView(View):
    template_name = 'account/forgot_password.html'
    form_class = ForgotPasswordForm
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email =form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            messages.success(request,'check your mail box','success')
            username =user.username
            return redirect('account:reset_password_email',username)
        return render(request,self.template_name,{'form':form})


# send email to users who forgotten their password and want to reset it:
def reset_password_email(request,username):
        user = User.objects.get(username=username)
        email = user.email
        send_mail(
            'peoplemedia.com - reset password',
            f' use link below to reset your password in peoplemedia.com \n\r'
            f' http://127.0.0.1:8000/reset-password/{user.username}',
            'pouriashaigani@gmail.com',
            recipient_list= [email],
            fail_silently=False,
        )
        return render(request,'account/reset_password_email.html',{'email':email})


# when user has validated his email for getting new password in last ClassView
# and redirected to this page for resetting his password:
class ResetPasswordView(View):
    template_name = 'account/reset_password.html'
    form_class = ResetPasswordForm
    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(username=kwargs['username'])
        return super().setup(request,*args,kwargs)
    def get(self,request,username):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request,username):
        form = self.form_class(request.POST)
        user = self.user_instance
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request,'your password changed successfully','success')
            return redirect('posts:home')