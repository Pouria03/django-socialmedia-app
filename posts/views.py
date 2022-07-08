import django.http
from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post,PostLike
from django.contrib import messages
from django.http import HttpResponseNotFound
from .forms import *
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class HomeView(View):
    form_class = SearchForm
    def get(self,request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request,'posts/home.html',{'posts':posts, 'search_form':self.form_class})



class PostDetailView(View):
    template_name = 'posts/detail.html'
    # comment form :
    form_class = CommentForm
    def get(self,request,post_id,slug):
        post = get_object_or_404(Post,pk=post_id,slug=slug)
        comments = post.PostComments.filter(is_reply=False)
        comment_form = self.form_class()
        context = {'post':post,'comment_form':comment_form,'comments':comments,}
        return render(request,self.template_name,context)

    @method_decorator(login_required())
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = request.user
            post = Post.objects.get(id=kwargs['post_id'])
            comment_form.post = post
            comment_form.save()
            messages.success(request,'your comment published')
            return redirect('posts:detail',kwargs['post_id'],kwargs['slug'])
        return django.http.HttpRequest('<p> validation failed </p')
# class bace view for deleting post :
class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
                return HttpResponseNotFound("404 - Not Found")
        user_id =request.user.id
        username = request.user.username
        if post.user.id == user_id:
            post.delete()
            messages.success(request,'post deleted !','success')
            return redirect('pages:profile',username)
        else:
            messages.warning(request,'you can\'t delete this post !','warning')
            return redirect('pages:profile',username)

        
class PostUpdateView(LoginRequiredMixin,View):
    template_name = 'posts/update.html'
    form_class = PostCreateUpdateForm

    def setup(self,request,*args,**kwargs):
        self.post_instance = get_object_or_404(Post,id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)


    def dispatch(self,request,*args,**kwargs):
        post = self.post_instance
        if request.user.id != post.user.id:
            messages.warning(request,'you can\'t update this post','warning')
            return redirect('posts:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request,self.template_name,{'form':form})

    def post(self,request,post_id):
        post = self.post_instance
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            updated_form =form.save(commit=False)
            updated_form.slug = slugify(form.cleaned_data.get('body')[:30])
            updated_form.save()
            return redirect('pages:profile',request.user.username)


class PostCreateView(View):
    template_name= 'posts/create.html'
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.user_instance =User.objects.get(username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs['username']:
            messages.warning(request, 'you can\'t create post for this user', 'warning')
            return redirect('posts:home')
        return super().dispatch(request, *args, **kwargs)
            
    def get(self,request,username):
        user = self.user_instance
        form = self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self,request,username):
        form = self.form_class(request.POST)
        if form.is_valid():
            created_form = form.save(commit=False)
            created_form.slug = slugify(form.cleaned_data.get('body')[:30])
            user = self.user_instance
            created_form.user = user
            created_form.save()
            messages.warning(request, 'your post createe successfully', 'success')
            return redirect('pages:profile',username)

        return render(request, self.template_name, {'form': form})



class PostLikeView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        like = PostLike.objects.filter(post=post,user = request.user)
        if like.exists():
            like.delete()
            return redirect('posts:detail',post.id , post.slug)
        else:
            PostLike.objects.create(post=post,user =request.user).save()
            return redirect('posts:detail',post.id , post.slug)


