from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from room_booking.models import Room


def delete_room(request: HttpRequest, room_id: int):
    """
        View to delete a specific room by its ID.

        Args:
            request (HttpRequest): The HTTP request object.
            room_id (int): The ID of the room to delete.

        Returns:
            HttpResponseRedirect: Redirects to the 'list_room' page after deletion.
        """

    # Retrieve the room by ID or return 404 if not found
    room = get_object_or_404(Room, id=room_id)

    # Delete the room instance from the database
    room.delete()

    # Redirect user to the list of rooms
    return redirect("list_room")

