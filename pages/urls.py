from django.urls import path
from . import views

app_name = 'pages'
urlpatterns= [
    path('profile/<str:username>'  ,views.UserProfileView.as_view(), name='profile'),
    path('follow/<str:username>/'  ,views.FollowUserView.as_view(),  name='follow'),
    path('Unfollow/<str:username>/',views.UnfollowUserView.as_view(),name='Unfollow'),
    path('followers/<str:username>',views.ShowFollowers.as_view(),name='followers'),
    path('followings/<str:username>',views.ShowFollowings.as_view(),name='followings'),
]