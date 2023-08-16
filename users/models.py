from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

USER_CHOICES = (
    (1,"Manager"),
    (2,"Team leader"),
    (3,"Team memeber"),
)

class CustomUser(AbstractUser):

  username= models.CharField(max_length=20, blank=True,unique = True)
  email = models.EmailField(unique = True)
  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  role=models.IntegerField(USER_CHOICES,default = '1')
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','role']
  
  
  def __str__(self):
      return "{}".format(self.email,self.role)
  

