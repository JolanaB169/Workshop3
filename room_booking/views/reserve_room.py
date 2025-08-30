from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from room_booking.models import Room, Reservation


def reserve_room(request: HttpRequest, room_id: int):
    """
        View to handle reservation of a room on a specific date.

        - Displays the reservation form with future reservations for the room.
        - Handles form submission, validates the date, checks availability,
          and creates a new reservation.

        Args:
            request (HttpRequest): The HTTP request object.
            room_id (int): The ID of the room to reserve.

        Returns:
            HttpResponse: Renders the reservation form or redirects to the room list on success.
        """

    # Retrieve the room or 404 if not found
    room = get_object_or_404(Room, id=room_id)

    # Get all future reservations for this room, ordered by date
    future_reservations = room.reservations.filter(date__gte=date.today()).order_by('date')
    if request.method == 'POST':
        booking_date = request.POST.get('date')
        comment = request.POST.get('comment')

        # Validate the date format
        try:
            booking_date_obj = date.fromisoformat(booking_date)
        except ValueError:
            messages.error(request, 'Zadejte platné datum.')
            return render(request, 'reserve_room.html',
                          {'room': room,
                           'reservations': future_reservations
                           })

        # Check that the booking date is not in the past
        if booking_date_obj < date.today():
            messages.error(request, 'Rezervace nelze provést zpětně.')
            return render(request, 'reserve_room.html',
                          {'room': room,
                           'reservations': future_reservations
                           })

        # Check if the room is already reserved on the requested date
        existing = room.reservations.filter(date=booking_date_obj).exists()
        if existing:
            messages.error(request, 'Místnost je již na tento den rezervována.')
            return render(request, 'reserve_room.html',
                          {'room': room,
                           'reservations': future_reservations
                           })

        # Create and save the new reservation
        reservation = Reservation(room=room, date=booking_date_obj, comment=comment)
        reservation.save()

        # Redirect to the room list view after successful reservation
        return redirect('list_room')

    else:
        # If GET request, display the reservation form with existing future reservations
        return render(request, 'reserve_room.html', {'room': room, 'reservations': future_reservations})

