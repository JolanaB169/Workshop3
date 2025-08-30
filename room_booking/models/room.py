from django.db import models


class Room(models.Model):
    """
    Model representing a room that can be reserved.

    Attributes:
        name (str): Name of the room.
        capacity (int): Maximum capacity of the room.
        projector (bool): Whether the room has a projector.
    """

    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name