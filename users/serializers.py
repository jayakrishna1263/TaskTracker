from users.models import CustomUser,Team,Task,TeamMember,TaskAssignment

from django.contrib.auth.models import User
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username','email','password','role']
        
    # def validate_username(self,data):
    #     special_characters="!@#$%^&*()-+=<>?/_"
    #     if any(c in special_characters for c in data['username']):
    #         raise serializers.ValidationError("Username should not contain special chars")
        
    def validate(self,data):
        if data['username']:
            if CustomUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username is taken")
    
        if data['email']:
            if CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email is taken")
        return data
    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'],role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data 
    
class TeamSerializer(serializers.ModelSerializer):
    team_lead=CustomUserSerializer()
    team_members=serializers.SerializerMethodField()
    # team_members=serializers.ListField(child=CustomUserSerializer(),read_only=True)
    # team_members = CustomUserSerializer(many=True, source='teammember_set.id')
    class Meta:
        model=Team
        fields=('team_name','team_members','team_lead')
        # depth=1
        
    def get_team_members(self,obj):
        team_id=obj.id
        team_members=TeamMember.objects.filter(team_id=team_id)
        print(team_members.values('member_id'))
        # serializer=CustomUserSerializer(team_members.values('member_id'),many=True)
        res=[]
        for member in team_members:
            res.append(CustomUserSerializer(member.member_id).data)
        # return serializer.data
        return res
        
    def validate_team_name(self,data):
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['team_name']):
            raise serializers.ValidationError("Team name should not contain special chars")
class TaskSerializer(serializers.ModelSerializer):
    task_memebers=CustomUserSerializer
    class Meta:
        model=Task
        fields="__all__"
        
    def validate_task_name(self,data):
        special_characters="!@#$%^&*()-+=<>?/_"
        if any(c in special_characters for c in data['task_name']):
            raise serializers.ValidationError("Task name should not contain special chars")
# class TeamMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=TeamMember
#         fields="__all__"
# class TaskAssignmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=TaskAssignment
#         fields="__all__"
        