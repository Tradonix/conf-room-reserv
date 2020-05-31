from datetime import datetime

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    has_projector = models.BooleanField(default=False)

    def is_reserved_today(self):
        today = datetime.today().date()
        return self.reserve_set.filter(date=today).count() > 0


class Reserve(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('date', 'room_id',)
