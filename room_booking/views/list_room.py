from django.http import HttpRequest
from django.shortcuts import render
from datetime import date
from room_booking.models import Room


def list_room(request: HttpRequest):
    """
        View that displays a list of all rooms with their reservation status for today.

        Retrieves all rooms from the database and checks whether each room
        is reserved on the current date. Passes the result to the template.

        Args:
            request (HttpRequest): The HTTP request from the user.

        Returns:
            HttpResponse: Renders the 'list_room.html' template with context containing
                          room data and today's reservation status.
        """
    rooms = Room.objects.all()  # Get all Room objects from the database
    today = date.today() # Get today's date

    room_data = []

    # Iterate through all rooms and check if they are reserved today
    for room in rooms:
        is_reserved_today = room.reservations.filter(date=today).exists()
        room_data.append({
            'room': room,
            'reserved': is_reserved_today
        })

    # Render the template with the room data
    return render(request, 'list_room.html', {
        'room_data': room_data,
    })
