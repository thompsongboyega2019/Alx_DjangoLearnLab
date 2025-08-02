from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='', null=True, blank=True)

# Create your models here.
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=200)
#     published_year = models.IntegerField()
    
    

    