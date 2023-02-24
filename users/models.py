from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    genders = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Custom', 'Custom'),
        ('Prefer not to say', 'Prefer not to say')
    ]
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        choices=genders, max_length=20, default="Unknown")


class Profile(models.Model):
    user = models.OneToOneField(
        'User', related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(default="", blank=True, null=True, max_length=75)
    follows = models.ManyToManyField(
        User, related_name='follows', blank=True, symmetrical=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_following(self):
        return self.follows.all()
