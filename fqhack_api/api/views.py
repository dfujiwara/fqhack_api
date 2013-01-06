from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from django.utils import simplejson
from django.views import generic

from api import models
from api import utils


class JsonResponse(HttpResponse):
    def __init__(self, content='', mimetype='application/json',
                 status=None, content_type=None):
        content = simplejson.dumps(content)
        super(JsonResponse, self).__init__(content=content, mimetype=mimetype,
                                           status=status, content_type=content_type)


class HttpResponseNoContent(HttpResponse):
    status_code = 204


def healthz(request):
    return HttpResponse("OK")


class EventsView(generic.View):
    """Event listing view."""
    def get(self, request):
        events = models.Event.objects.all()
        event_content_list = [utils.event_to_dict(e) for e in events]
        return JsonResponse(event_content_list)

    def post(self, request):
        """Creates an event.""" 
        user_id = request.user_id
        venue_id = request.POST.get('venue_id')
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        event_description = request.POST.get('event_description')
        scope = request.POST.get('scope', models.Event.SCOPE_PUBLIC)

        if utils.validate_args([user_id, venue_id, title,
                                event_date, event_description, scope]):
            utils.log('View error: missing args')
            return HttpResponseBadRequest()

        # Convert the timestamp to datetime
        try:
            event_date = float(event_date)
        except:
            utils.log('View error: event_date is invalid')
            return HttpResponseBadRequest()

        event_date = utils.get_datetime(event_date)

        models.Event.objects.create(organizer_id=user_id,
                                    venue_id=venue_id,
                                    title=title,
                                    event_date=event_date,
                                    event_description=event_description,
                                    scope=scope)
        return HttpResponseNoContent()
        


class EventView(generic.View):
    """Single event view."""
    def get(self, request, event_id):
        """Gets the event detail."""
        try:
            event = models.Event.objects.select_related('organizer').get(
                id=event_id)
        except models.Event.DoesNotExist:
            return HttpResponseBadRequest()
   
        event_content = utils.event_to_dict(event)
 
        comments = models.Comment.objects.filter(
            event__id=event.id).select_related('user')
        comment_content_list = [utils.comment_to_dict(c) for c in comments]

        attendees = models.Attendance.objects.filter(
            event__id=event.id).select_related('user')
        attendee_list = [utils.attendance_to_dict(a) for a in attendees]

        response_content = {'event': event_content,
                            'comments': comment_content_list,
                            'attendees': attendee_list}
        return JsonResponse(response_content)


class CommentView(generic.View):
    """Comment view."""
    def post(self, request, event_id):
        user_id = request.user_id
        comment = request.POST.get('comment')

        if utils.validate_args([event_id, user_id, comment]):
            utils.log('View error: missing args')
            return HttpResponseBadRequest()
        
        # Create the comment object.
        models.Comment.objects.create(event_id=event_id, user_id=user_id, 
                                      comment=comment)
        return HttpResponseNoContent()
        

class AttendanceView(generic.View):
    """Attendance view."""
    def post(self, request, event_id):
        user_id = request.user_id
        attendance_flag = request.POST.get('attendance')

        if utils.validate_args([event_id, user_id, attendance_flag]):
            utils.log('View error: missing args')
            return HttpResponseBadRequest()

        try:
            attendance_flag = int(attendance_flag)
        except ValueError:
            return HttpResponseBadRequest()

        if attendance_flag not in (models.Attendance.ATTENDING, 
                                   models.Attendance.NOT_ATTENDING):
            return HttpResponseBadRequest()
        
        attendance, created = models.Attendance.objects.get_or_create(
            event__id=event_id,
            user__id=user_id,
            defaults={'event_id': event_id, 
                     'user_id': user_id,
                     'attendance': attendance_flag})

        if not created:
            attendance.attendance = attendance_flag
            attendance.save()

        return HttpResponseNoContent()
