from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from datetime import date
from room_booking.models import Room



def detail_room(request: HttpRequest, room_id: int):
    """
        View that displays details for a specific room, including its future reservations.

        Args:
            request (HttpRequest): The HTTP request from the client.
            room_id (int): The ID of the room to display.

        Returns:
            HttpResponse: Renders the 'detail_room.html' template with the room and its future reservations.
        """

    # Retrieve the room by ID or return 404 if not found
    room = get_object_or_404(Room, id=room_id)

    # Get all reservations for this room from today onward, sorted by date
    future_reservations = room.reservations.filter(date__gte=date.today()).order_by('date')

    # Render the detail page with room and reservation info
    return render(request, 'detail_room.html', {
        'room': room,
        'reservations': future_reservations
    })
