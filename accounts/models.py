from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/', blank=True, null=True, default='user.png')
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
