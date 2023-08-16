from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = CustomUser
    list_display = ('id','username','email', 'first_name',
                    'role')

admin.site.register(CustomUser,UserAdminConfig)


