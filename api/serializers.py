from users.models import *

from django.contrib.auth.models import User
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"
        #fields=['username','email','role']
        
    def validate_username(self,data):
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['username']):
            raise serializers.ValidationError("Username should not contain special chars")
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields="__all__"
        
    def validate_team_name(self,data):
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['team_name']):
            raise serializers.ValidationError("Team name should not contain special chars")
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields="__all__"
        
    def validate_username(self,data):
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['task_name']):
            raise serializers.ValidationError("Task name should not contain special chars")
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamMember
        fields="__all__"
class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskAssignment
        fields="__all__"
        