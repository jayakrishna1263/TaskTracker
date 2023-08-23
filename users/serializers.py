from users.models import CustomUser,Team,Task,TeamMember,TaskAssignment

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
    
    class Meta:
        model=Team
        fields=('team_name','team_lead','team_members')
        
    def get_team_members(self,obj):
        # print(obj)
        team_members=TeamMember.objects.filter(team_id=obj.id)
        print(team_members.values('member_id'))
        res=[]
        for member in team_members:
            res.append(CustomUserSerializer(member.member_id).data)
        return res
    
    def create(self, validated_data):   
        team=Team.objects.create(team_name=validated_data['team_name'],team_lead=validated_data['team_lead'])
        for team_member in validated_data['team_members']:
            TeamMember.objects.create(team_id=team,member_id=team_member)
        # print(TeamMember.objects.all())
        team.save()
        return team 
    
    def update(self, instance, validated_data): 
        #To update Team lead
        team_lead_username = self.initial_data.get('team_lead')
        # print(team_lead_username)
        if team_lead_username:
            team_lead= CustomUser.objects.get(username=team_lead_username)
            instance.team_lead = team_lead


        #To add members
        members_to_add=self.initial_data.get('members_add')
        if members_to_add:
            for member_username in members_to_add:
                member=get_object_or_404(CustomUser,username=member_username,role="Team member")
                if not TeamMember.objects.filter(team_id=instance, member_id=member).exists():    
                    TeamMember.objects.create(team_id=instance,member_id=member)
                else:
                    raise serializers.ValidationError(f"{member_username} is  already exists team {instance}")
        
        #To remove members
        members_to_remove=self.initial_data.get('members_remove')
        if members_to_remove:
            for member_username in members_to_remove:
                member=get_object_or_404(CustomUser,username=member_username,role="Team member")
                team_member_instance=TeamMember.objects.filter(team_id=instance, member_id=member)
                if team_member_instance:    
                    team_member_instance.delete()
                else:
                    raise serializers.ValidationError(f"{member_username} is  not part of team {instance}")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # instance.team_name = validated_data.get('team_name', instance.team_name)
        
        instance.save()
        return instance

      

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
        
    def create(self, validated_data):
        
        task=Task.objects.create(**validated_data)
        
        team_id = validated_data.get("team_id")
        team_members=TeamMember.objects.filter(team_id=team_id)
        task_members_usernames = self.initial_data.get('task_members')
        team_members_usernames = [member.member_id.username for member in team_members]
            
        task_members=[]
        for member_username in task_members_usernames:
                # print("******")
                # print(member_username,team_members_usernames)
                if member_username in team_members_usernames:
                    
                    task_members.append(get_object_or_404(CustomUser,username=member_username))
                else:
                    raise serializers.ValidationError(f"{member_username} is  not part of team {team_id}")
        
        for task_member in task_members:
            TaskAssignment.objects.create(task_id=task,member_id=task_member)
        task.save()
        return task

    def update(self,instance,validated_data):
        #To update team
        team_id=self.initial_data.get("team_id")
        if team_id:
            team=Team.objects.get(id=team_id)
            instance.team_id=team
        
        #Add task members
        task_members_to_add=self.initial_data.get("members_add")
        if task_members_to_add:
            for member_username in task_members_to_add:
                member=get_object_or_404(CustomUser,username=member_username,role="Team member")
                if not TaskAssignment.objects.filter(task_id=instance,member_id=member).exists():
                    TaskAssignment.objects.create(task_id=instance,member_id=member)
                else:
                    raise serializers.ValidationError(f"{member} already exists in task {instance}")
        
        #Remove task members
        task_members_to_remove=self.initial_data.get("members_remove")
        if task_members_to_remove:
            for member_username in task_members_to_remove:
                member=get_object_or_404(CustomUser,username=member_username,role="Team member")
                assignment_instance=TaskAssignment.objects.filter(task_id=instance,member_id=member)
                if assignment_instance:
                    assignment_instance.delete()
                else:
                    raise serializers.ValidationError(f"{member} does not assigned for task {instance}")
        
        #To set all other attributes
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
            
        instance.save()
        return instance