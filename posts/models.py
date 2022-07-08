from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.votes.count()

    def __str__(self):
        return f'{self.slug} -{self.user.username} -  {self.created_date.strftime("%h/%d/%Y - %H:%M")}'

    class Meta:
        ordering = ('-id',)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserPosts')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='PostComments')
    replied_comment = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='replies')
    body = models.CharField(max_length=400)
    is_reply = models.BooleanField(default=False)
    date_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:5]} - {self.date_comment.strftime("%h/%d/%Y - %H:%M")}'

    class Meta:
        ordering = ('-date_comment',)


class PostLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='votes')

    def __str__(self):
        return f'{self.user} liked {self.post}'
