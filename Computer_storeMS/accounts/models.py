from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),    
    )
    
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    phone =models.CharField(max_length=15)
    address=models.TextField()
    role =models.CharField(max_length=10, choices=ROLE_CHOICES,default='customer')
    def __str__(self):
        return self.user.username
# Create your models here.
