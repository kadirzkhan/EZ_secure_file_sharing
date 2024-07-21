# /models.py
from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission

class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='secure_file_sharing_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='secure_file_sharing_user_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class File(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)