from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Room, reservation

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


def list_room(request):
    rooms = Room.objects.all()
    today = date.today()

    room_data = []
    for room in rooms:
        is_reserved_today = room.reservations.filter(date=today).exists()
        room_data.append({
            'room': room,
            'reserved': is_reserved_today
        })

    return render(request, 'list_room.html', {
        'room_data': room_data,
    })

def detail_room(request: HttpRequest, room_id):
    room = get_object_or_404(Room, id=room_id)
    future_reservations = room.reservations.filter(date__gte=date.today()).order_by('date')

    return render(request, 'detail_room.html', {
        'room': room,
        'reservations': future_reservations
    })


def modify_room(request: HttpRequest, room_id):
    room = get_object_or_404(Room, id=room_id)
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
            room.name = name
            room.capacity = int(capacity)
            room.projector = projector
            room.save()
            return redirect("list_room")
    return render(request, 'modify_room.html', {
        'room': room,
    })

def delete_room(request: HttpRequest, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect("list_room")

def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    future_reservations = room.reservations.filter(date__gte=date.today()).order_by('date')
    if request.method == 'POST':
        booking_date = request.POST.get('date')
        comment = request.POST.get('comment')

        try:
            booking_date_obj = date.fromisoformat(booking_date)
        except ValueError:
            messages.error(request, 'Zadejte platné datum.')
            return render(request, 'reserve_room.html', {'room': room, 'reservations': future_reservations})

        if booking_date_obj < date.today():
            messages.error(request, 'Rezervace nelze provést zpětně.')
            return render(request, 'reserve_room.html', {'room': room, 'reservations': future_reservations})

        existing = room.reservations.filter(date=booking_date_obj).exists()
        if existing:
            messages.error(request, 'Místnost je již na tento den rezervována.')
            return render(request, 'reserve_room.html', {'room': room, 'reservations': future_reservations})

        reservation = Reservation(room=room, date=booking_date_obj, comment=comment)
        reservation.save()
        return redirect('list_room')
    else:
        return render(request, 'reserve_room.html', {'room': room, 'reservations': future_reservations})

def search_room(request):
    name = request.GET.get('name', '').strip()
    capacity = request.GET.get('capacity')
    projector = request.GET.get('projector')
    today = date.today()

    rooms = Room.objects.all()

    if name:
        rooms = rooms.filter(name__icontains=name)
    if capacity and capacity.isdigit():
        rooms = rooms.filter(capacity__gte=int(capacity))
    if projector:
        rooms = rooms.filter(projector=True)

    available_rooms = []
    for room in rooms:
        if not room.reservations.filter(date=today).exists():
            available_rooms.append(room)

    context = {
        'rooms': available_rooms,
        'searched': True
    }

    return render(request, 'search_results.html', context)