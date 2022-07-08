from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # all posts
    path('',views.HomeView.as_view(),name='home'),
    # post detail
    path('post/<int:post_id>/<slug:slug>/',views.PostDetailView.as_view(),name='detail'),
    # delete post
    path('post/delete/<int:post_id>/',views.PostDeleteView.as_view(),name='delete'),
    # update post
    path('post/update/<int:post_id>/',views.PostUpdateView.as_view(),name='update'),
    # create post
    path('post/create/<str:username>',views.PostCreateView.as_view(),name='create'),
    # like url:
    path('like/<int:post_id>/',views.PostLikeView.as_view(),name='like')
]