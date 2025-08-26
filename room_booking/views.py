from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from .models import Room

def home_page_view(request):
    return render(request, 'home.html')

def add_room(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == 'on'

        if not name:
            messages.error(request, "Prosím zadej název místonosti.")
        elif Room.objects.filter(name=name).exists():
            messages.error(request, "Místnost s tímto názvem již existuje.")
        elif not capacity.isdigit() or int(capacity) <= 0:
            messages.error(request, "Kapacita musí být kladné číslo.")
        else:
            Room.objects.create(
                name=name,
                capacity=int(capacity),
                projector=projector
            )
            messages.success(request, "Místnost přidána.")
            return redirect("list_room")
    return render(request, 'add_room.html')


def list_room(request: HttpRequest):
    rooms = Room.objects.all()
    today = now().date()

    return render(request, 'list_room.html', {
        'rooms': rooms,
        'today': today,
    })

def detail_room(request: HttpRequest):
    pass


def modify_room(request: HttpRequest):
    pass

def delete_room(request: HttpRequest, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect("list_room")

def reserve_room(request: HttpRequest):
    pass
