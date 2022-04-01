from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class LinkedinUserManager(BaseUserManager):
    def create_user(self,email,name, job_title,password=None):
        if not email:
            raise ValueError('Email is required!')
        if not name:
            raise ValueError('Name is required!')
        if not job_title:
            raise ValueError('Job title is required!')
        # if not name.isalpha():
        #     raise ValueError('Name should only contain letters!')
        if len(name)<4:
            raise ValueError('Name should contain at least 4 letters!')
        # if not job_title.isalpha():
        #     raise ValueError('Job title should only contain letters!')
        if len(job_title)<14:
            raise ValueError('Job title should contain at least 14 letters!')
        user= self.model(
            email=self.normalize_email(email),
            name=name,
            job_title=job_title
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name, job_title,password=None):
        user=self.create_user(email=self.normalize_email(email),name=name,job_title=job_title,password=password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user



class LinkedinUser(AbstractBaseUser):
    name=models.CharField(verbose_name='Name', max_length=50)
    email=models.EmailField(verbose_name='Email address', max_length=50, unique=True)
    job_title= models.CharField(verbose_name='Job Title', max_length=100)
    date_joined=models.DateField(verbose_name='Date joined',auto_now_add=True)
    last_login=models.DateField(verbose_name='Last login',auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['job_title','name']

    objects= LinkedinUserManager()

    def __str__(self):
        return self.name
    def has_perm(self, perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
