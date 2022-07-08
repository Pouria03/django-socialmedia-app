from django.urls import path
from . import views

app_name='account'
urlpatterns =[
    path('register/',views.RegisterUser.as_view(),name='register'),
    path('login/',views.LoginUserView.as_view(),name='login'),
    path('logout/',views.UserLogOutView.as_view(),name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<str:username>/',views.ResetPasswordView.as_view(),name='reset_password'),
    path('password-email-sent/<str:username>/',views.reset_password_email,name='reset_password_email'),
]