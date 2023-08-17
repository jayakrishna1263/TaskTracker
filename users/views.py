from users.models import *
from .serializers import *

from django.shortcuts import render
from django.core.paginator import Paginator

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


