
from django.db import models
from . import manager
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,PermissionsMixin

# Create your models here.

USER_CHOICES = (
    ("Manager","Manager"),
    ("Team leader","Team leader"),
    ("Team member","Team member"),
)
STATUS_CHOICES = (
    ("Created","Created"),
    ("Assigned","Assigned"),
    ("In Progrss","In Progrss"),
    ("Under Review","Under Review"),
    ("Done","Done"),
)

class CustomUser(AbstractUser,PermissionsMixin):

  username= models.CharField(max_length=20, blank=True,unique = True)
  email = models.EmailField(unique = True)
  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  role=models.CharField(choices=USER_CHOICES,default = 'Manager',max_length=100)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','role']
  
  def __str__(self):
      return "{}".format(self.username)
  
class Team(models.Model):
    team_name=models.CharField(max_length=100,unique = True)
    team_lead=models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'role': "Team leader"})
    
    class Meta:
       unique_together = ("team_name", "team_lead")
    
    def __str__(self):
      return self.team_name
class Task(models.Model):
    task_name=models.CharField(max_length=100)
    team_id=models.ForeignKey(Team, on_delete=models.SET_NULL,null=True)
    status=models.CharField(choices=STATUS_CHOICES,default = 'Created',max_length=100)
    start_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(null=True,blank=True)

    @property
    def is_completed(self):
        return self.status == "Done"
    def save(self, *args, **kwargs):
        if self.status == "Done" and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != "Done" :
            self.completed_at = None
        super().save(*args, **kwargs)
        
    
    def __str__(self):
      return self.task_name

class TeamMember(models.Model):
    team_id=models.ForeignKey(Team, on_delete=models.CASCADE)
    member_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'role': "Team member"})
    
    
    class Meta:
       unique_together = ("team_id","member_id")
    
    def __str__(self):
      return "{}".format(str(self.team_id)+" "+str(self.member_id))
  


class TaskAssignment(models.Model):
    task_id=models.ForeignKey(Task, on_delete=models.CASCADE)
    member_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'role': "Team member"})
    
    class Meta:
       unique_together = ("task_id", "member_id")
    def __str__(self):
      return "{}".format(str(self.task_id)+" "+str(self.member_id))

