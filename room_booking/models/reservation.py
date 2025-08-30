from django.db import models
from .room import Room

class Reservation(models.Model):
    """
    Model representing a reservation of a room on a specific date.

    Attributes:
        date (date): The reservation date.
        room (Room): The room being reserved.
        comment (str): Optional comment regarding the reservation.

    Constraints:
        Unique together: (room, date) - a room can be reserved only once per day.
    """

    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    comment = models.TextField()
    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return f"{self.room.name} - {self.date}"