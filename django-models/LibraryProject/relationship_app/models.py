# from django.db import models

# # Create your models here.
# class Author(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)

# class Library(models.Model):
#     name = models.CharField(max_length=255)
#     books = models.ManyToManyField(Book, related_name='book')

# class Librarian(models.Model):
#     name = models.CharField(max_length=255)
#     library = models.OneToOneField(Library, on_delete=models.CASCADE)


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    UserProfile model to extend Django's built-in User model with role-based access control.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile when the User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)