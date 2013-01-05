from django.contrib.auth import models as auth_models
from django.db import models


class APIUser(models.Model):
    """User model."""
    user = models.ForeignKey(auth_models.User, unique=True)
    token = models.CharField(max_length=100)


class Event(models.Model):
    """Event model."""
    venue_id = models.IntegerField(unique=True)
    event_date = models.DateTimeField()


class Comment(models.Model):
    """Comment model associated with specific user and event."""
    event = models.ForeignKey(Event)
    user = models.ForeignKey(APIUser)
    comment = models.TextField()


class Attendance(models.Model):
    """Attendance model associated with specific user and event."""
    event = models.ForeignKey(Event)
    user = models.ForeignKey(APIUser)
    
    ATTENDING = 1
    NOT_ATTENDING = 2

    ATTENDANCE_CHOICES = (
        (ATTENDING, 'Attending'),
        (NOT_ATTENDING, 'Not attending')
    )
    attendance = models.SmallIntegerField()

    class Meta:
        unique_together = ('event', 'user') 
