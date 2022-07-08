from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from .models import Relation


# Create your views here.
class UserProfileView(LoginRequiredMixin,View):
    is_following = False
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user)

        relation = Relation.objects.filter(from_user=request.user,to_user=user).exists()
        if relation:
            self.is_following = True
        context= {'user': user,
                  'posts': posts,
                  'is_following':self.is_following
                  }
        return render(request, 'pages/profile.html',context)


# this class represents operation of following somebody:
class FollowUserView(LoginRequiredMixin,View):
    def get(self, request, username):
        from_user = request.user
        to_user = User.objects.get(username=username)
        relation= Relation.objects.filter(from_user=from_user, to_user=to_user)
        if not relation.exists():
            relation = Relation(from_user=from_user, to_user=to_user).save()
            messages.success(request, f'you are following {to_user}', 'success')
            return redirect('pages:profile', to_user.username)

        else:
            messages.info(request, f'you are already following {to_user}', 'info')
            return redirect('pages:profile', to_user.username)


# this class represents operation of Unfollowing someone:
class UnfollowUserView(LoginRequiredMixin,View):
    def get(self, request, username):
        to_user = User.objects.get(username=username)
        from_user = request.user
        relation = Relation.objects.filter(from_user=from_user,to_user=to_user)
        if relation.exists():
            relation.delete()
            messages.success(request,f'you Unfollowed {username}','success')
            return redirect('pages:profile',username)
        else:
            messages.warning(request,'you are not following this user ','warning')
            return redirect('pages:profile',username)

class ShowFollowers(View):
    template_name = 'pages/followers.html'
    def get(self,request,username=None):
        user = User.objects.get(username=username)
        if user != None:
           followers = Relation.objects.filter(to_user=user)

        return render(request,self.template_name,{'followers':followers})

class ShowFollowings(View):
    template_name = 'pages/followings.html'
    def get(self,request,username=None):
        user = User.objects.get(username=username)
        if user != None:
           followings = Relation.objects.filter(from_user=user)

        return render(request,self.template_name,{'followings':followings})