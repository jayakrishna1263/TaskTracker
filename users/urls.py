from .views import *

from django.urls import path,include

urlpatterns = [
    path("users-list",CustomUserAPI.as_view(),name="CustomUser"),
    path("team",TeamAPI.as_view(),name="Teams"),
]