from .views import *

from django.urls import path,include

urlpatterns = [
    path("users",CustomUserAPI.as_view(),name="CustomUser"),
    path("team",TeamAPI.as_view(),name="Teams"),
    path("task",TaskAPI.as_view(),name="Tasks"),
]