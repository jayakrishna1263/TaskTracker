from users.models import *
from .serializers import *

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

# Create your views here.

class CustomUserAPI(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, BasicAuthentication]
    def get(self,request):
        objs=CustomUser.objects.all()
        serializer =CustomUserSerializer(objs,many=True)
        print(request.user)
        return Response(serializer.data)
    def post(self,request):
        data=request.data
        serializer=CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )

class TeamAPI(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, BasicAuthentication]
    def get(self,request):
        objs=Team.objects.all()
        serializer =TeamSerializer(objs,many=True)
        print(request.user)
        return Response(serializer.data)
    def post(self,request):
        data=request.data
        team_lead=get_object_or_404(CustomUser,username=data.get('team_lead'))

        team_members=[]
        for member in data.get('team_members'):
            team_members.append(CustomUser.objects.get(username=member))
        serializer=TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save(team_lead=team_lead,team_members=team_members)
            # print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request):
        data=request.data
        team=get_object_or_404(Team,team_name=data.get('team_name'))

        serializer=TeamSerializer(team,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self,request):
        data=request.data
        team=get_object_or_404(Team,team_name=data.get('team_name'))

        serializer=TeamSerializer(team,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class TaskAPI(APIView):
    def get(self,request):
        objs=Task.objects.all()
        serializer =TaskSerializer(objs,many=True)
        print(request.user)
        return Response(serializer.data)
    def post(self,request):
        data=request.data
        team_id=get_object_or_404(Team,id=data.get('team_id'))
        
        serializer=TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(team_id=team_id)
            # print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)
    def put(self,request):
        data=request.data
        task=get_object_or_404(Task,task_name=data.get('task_name'))

        serializer=TaskSerializer(task,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self,request):
        data=request.data
        task=get_object_or_404(Task,task_name=data.get('task_name'))

        serializer=TaskSerializer(task,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

