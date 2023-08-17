from users.models import *

from django.contrib.auth.models import User
from rest_framework import serializers

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"
        #exclude=['name']
        #fields=['name','age']
        # depth=1
        
    # def validate(self,data):  # Here data=[id,name,age]
    #     if data['age']<18:
    #         raise serializers.ValidationError("age should be greater than 18")
    #     return data
    # def validate_age(self,data):   #Here data=age
    #     if data<18:
    #         raise serializers.ValidationError("age should be greater than 18")
    #     return data