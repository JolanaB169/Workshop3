from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from room_booking.models import Room



def modify_room(request: HttpRequest, room_id: int):
    """
        View for modifying an existing room.

        Allows the user to update the room's name, capacity, and projector availability.
        Displays a form for GET requests, and processes form data on POST.

        Args:
            request (HttpRequest): The HTTP request object.
            room_id (int): ID of the room to be modified.

        Returns:
            HttpResponse: Renders the 'modify_room.html' form template,
                          or redirects to the room list on successful update.
        """

    # Try to get the room by ID or show 404 if not found
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        # Get form data from POST request
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == 'on'

        # Validate form inputs
        if not name:
            messages.error(request, "Prosím zadej název místonosti.")
        # Ensure the name is unique – allow current room name
        elif Room.objects.filter(name=name).exclude(id=room.id).exists():
            messages.error(request, "Místnost s tímto názvem již existuje.")
        elif not capacity.isdigit() or int(capacity) <= 0:
            messages.error(request, "Kapacita musí být kladné číslo.")
        else:
            # Update and save the room
            room.name = name
            room.capacity = int(capacity)
            room.projector = projector
            room.save()
            return redirect("list_room")

    # For GET requests or if validation fails, render the form again
    return render(request, 'modify_room.html', {
        'room': room,
    })

