from django.urls import path
from .views import add_room



urlpatterns = [
    path('room/new', add_room, name='add_room'),



]