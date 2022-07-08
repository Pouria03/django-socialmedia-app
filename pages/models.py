from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# this model represents the operation of 'following' of profiles:
class Relation(models.Model):
    # user that follows:
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    # user that has been followed:
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followings')
    start_following_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} followed {self.to_user} at {self.start_following_date.strftime("%h/%d/%Y - %H:%M")}'

