from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room

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
            return redirect("room_list")
    return render(request, 'add_room.html')




