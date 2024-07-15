from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model() 
# Create your models here.

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True)
    feedback = models.TextField(max_length=7000)
    time_submitted = models.DateTimeField(auto_now_add=True)