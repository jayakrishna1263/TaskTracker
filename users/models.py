from datetime import timezone
from django.db import models
from . import manager

from django.contrib.auth.models import AbstractUser,PermissionsMixin

# Create your models here.

USER_CHOICES = (
    (1,"Manager"),
    (2,"Team leader"),
    (3,"Team memeber"),
)
STATUS_CHOICES = (
    (1,"Created"),
    (2,"Assigned"),
    (3,"In Progrss"),
    (4,"Under Review"),
    (5,"Done"),
)

class CustomUser(AbstractUser,PermissionsMixin):

  username= models.CharField(max_length=20, blank=True,unique = True)
  email = models.EmailField(unique = True)
  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  role=models.IntegerField(USER_CHOICES,default = '1')
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','role']
  
  def __str__(self):
      return "{}".format(self.email,self.role)
  
class Team(models.Model):
    team_name=models.CharField(max_length=100,unique = True)
    team_lead=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="team",limit_choices_to={'role': 2})
    
    class Meta:
       unique_together = ("team_name", "team_lead")
    
    def __str__(self):
      return "{}".format(self.team_name,self.team_lead)
  


