from users.models import CustomUser,Team,Task,TeamMember,TaskAssignment

from django.contrib.auth.models import User
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username','email','password','role']
        
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
    team_lead=CustomUserSerializer(read_only=True)
    team_members=serializers.SerializerMethodField(read_only=True)
    # team_members=serializers.ListField(child=CustomUserSerializer(),read_only=True)
    # team_members = CustomUserSerializer(many=True, source='teammember_set.id')
    class Meta:
        model=Team
        fields=('team_name','team_members','team_lead')
        read_only_fields=('team_members','team_lead')
        
    def get_team_members(self,obj):
        team_members=TeamMember.objects.filter(team_id=obj.id)
        print(team_members.values('member_id'))
        # serializer=CustomUserSerializer(team_members.values('member_id'),many=True)
        res=[]
        for member in team_members:
            res.append(CustomUserSerializer(member.member_id).data)
        # return serializer.data
        return res
    def to_representation(self, instance):
        self.fields['team_lead'] =  CustomUserSerializer(read_only=True)
        # self.fields['team_members'] =  CustomUserSerializer(read_only=True)
        return super(TeamSerializer, self).to_representation(instance)
      
    # def validate_team_name(self,data):
    #     special_characters="!@#$%^&*()-+=<>?/_"
    #     if any(c in special_characters for c in data['team_name']):
    #         raise serializers.ValidationError("Team name should not contain special chars")
class TaskSerializer(serializers.ModelSerializer):
    # team_id=TeamSerializer(read_only=True)
    task_members=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Task
        fields=('task_name','team_id','status','start_at','completed_at','task_members')
        
    def get_task_members(self,obj):
        task_members=TaskAssignment.objects.filter(task_id=obj.id)
        # print(task_members.values('member_id'))
        res=[]
        for member in task_members:
            res.append(CustomUserSerializer(member.member_id).data)
        return res    
    
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
        