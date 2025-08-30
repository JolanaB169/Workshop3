from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from room_booking.models import Room

def add_room(request: HttpRequest):
    """
       View for adding a new room to the system.

       Handles both GET and POST requests:
       - GET: renders a form for entering room details.
       - POST: processes the form, validates input, and saves the room to the database.

       Args:
           request (HttpRequest): The HTTP request object from the user.

       Returns:
           HttpResponse: Renders 'add_room.html' or redirects to 'list_room' upon successful submission.
       """
    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == 'on' # Checkbox returns 'on' if checked

        # Validate input
        if not name:
            messages.error(request, "Prosím zadej název místonosti.") # Name is required
        elif Room.objects.filter(name=name).exists():
            messages.error(request, "Místnost s tímto názvem již existuje.") # Name must be unique
        elif not capacity.isdigit() or int(capacity) <= 0:
            messages.error(request, "Kapacita musí být kladné číslo.") # Capacity must be a positive number
        else:
            # Create new Room object
            Room.objects.create(
                name=name,
                capacity=int(capacity),
                projector=projector
            )
            messages.success(request, "Místnost přidána.") # Confirmation message
            return redirect("list_room")# Redirect to room list view

    # For GET request or if form has errors, show the form again
    return render(request, 'add_room.html')
