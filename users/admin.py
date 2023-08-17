from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

# Register your models here.
class UserAdminConfig(admin.ModelAdmin):
    model = CustomUser
    list_display = ('id','username','password','email', 'first_name',
                    'role')
    fields=['username','email','password','role']
class TeamAdminConfig(admin.ModelAdmin):
    model = Team
    list_display = ('id','team_name','team_id', 'status',
                    'start_at')
class TaskAdminConfig(admin.ModelAdmin):
    model = Task
    list_display = ('id','task_name','team_id', 'status',
                    'start_at','completed_at')


admin.site.register(CustomUser,UserAdminConfig)
admin.site.register(Team)
admin.site.register(Task,TaskAdminConfig)
admin.site.register(TeamMember)
admin.site.register(TaskAssignment)


