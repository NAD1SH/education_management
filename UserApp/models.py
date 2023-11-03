from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class UserProfile(AbstractUser):
    ROLE_CHOICES = {
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('principal', 'Principal')
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username 
