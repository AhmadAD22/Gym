from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

    
class UserManager(BaseUserManager):
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractUser):
    username=None
    fullName = models.CharField(max_length=255, blank=False)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10,unique=True)
    is_active=models.BooleanField(default=True,blank=True)
    is_staff=models.BooleanField(default=False,blank=True)
    is_superuser=models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True,null=True)
   
    USERNAME_FIELD = 'phone'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS = []
    objects = UserManager()
 


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    device_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.device_id}"