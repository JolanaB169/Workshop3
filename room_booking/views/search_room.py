from django.http import HttpRequest
from django.shortcuts import render
from datetime import date
from room_booking.models import Room


def search_room(request: HttpRequest):
    """
        View to search for available rooms based on optional filters: name, capacity, and projector availability.

        It returns rooms that match the filters and are not reserved for today's date.

        Args:
            request (HttpRequest): The HTTP GET request containing search parameters.

        Returns:
            HttpResponse: Renders 'search_results.html' with the filtered and available rooms.
        """

    # Retrieve search parameters from GET request, with default values
    name = request.GET.get('name', '').strip()
    capacity = request.GET.get('capacity')
    projector = request.GET.get('projector')
    today = date.today()

    # Start with all rooms
    rooms = Room.objects.all()

    # Filter rooms by name (case-insensitive substring match) if name provided
    if name:
        rooms = rooms.filter(name__icontains=name)

    # Filter rooms with capacity greater or equal if capacity is valid digit
    if capacity and capacity.isdigit():
        rooms = rooms.filter(capacity__gte=int(capacity))

    # Filter rooms that have a projector if the checkbox/filter is set
    if projector:
        rooms = rooms.filter(projector=True)

    # Filter out rooms that are reserved today
    available_rooms = []
    for room in rooms:
        if not room.reservations.filter(date=today).exists():
            available_rooms.append(room)

    context = {
        'rooms': available_rooms,
        'searched': True # Flag to indicate search was performed
    }

    # Render the search results page with the available rooms
    return render(request, 'search_results.html', context)