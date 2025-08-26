from django.urls import path
from .views import home_page_view, add_room, list_room, detail_room, modify_room, delete_room, reserve_room



urlpatterns = [
    path('', home_page_view, name='home'),
    path('room/new', add_room, name='add_room'),
    path('room/list', list_room, name='list_room'),

path('room/<int:room_id>/', detail_room, name='detail_room'),
path('room/modify/<int:room_id>/', modify_room, name='modify_room'),
path('room/delete/<int:room_id>/', delete_room, name='delete_room'),
path('room/reserve/<int:room_id>/', reserve_room, name='reserve_room'),



]