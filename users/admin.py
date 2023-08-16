from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

# Register your models here.
class UserAdminConfig(admin.ModelAdmin):
    model = CustomUser
    list_display = ('id','username','email', 'first_name',
                    'role')
    fields=['username','email','password','role']


admin.site.register(CustomUser,UserAdminConfig)
admin.site.register(Team)


