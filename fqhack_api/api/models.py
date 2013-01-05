from django.contrib.auth import models as auth_models
from django.db import models


class APIUser(models.Model):
    """User model."""
    user = models.ForeignKey(auth_models.User, unique=True)
    token = models.CharField(max_length=100)

    def __uniocode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


class Event(models.Model):
    """Event model."""
    # The venue id should be the fq venue id
    venue_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=250)
    event_date = models.DateTimeField()
    event_description = models.TextField()
    organizer = models.ForeignKey(APIUser)
    creation_date = models.DateTimeField(auto_now_add=True)

    SCOPE_PUBLIC = 1
    SCOPE_PRIVATE = 2
    SCOPE_CHOICES = (
        (SCOPE_PUBLIC, 'Public'),
        (SCOPE_PRIVATE, 'Private')
    )
    scope = models.SmallIntegerField()


class Comment(models.Model):
    """Comment model associated with specific user and event."""
    event = models.ForeignKey(Event)
    user = models.ForeignKey(APIUser)
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)


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
