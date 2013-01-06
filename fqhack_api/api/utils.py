import time

from api import models


def get_timestamp(datetime):
    # Note that the datetime objects are converted to timestamp
    return time.mktime(datetime.timetuple())


def validate_args(args):
    """Returns True or False based on whether all args were provided."""
    # Check if all required args are provided.
    args_list = [event_id, user_id, comment]
    filtered_args = filter(None, args_list)
    return len(args_list) != len(filtered_args)


def user_to_dict(user):
    user_dict = {}
    user_dict['id'] = user.id
    user_dict['name'] = user.full_name()
    return user_dict    


def event_to_dict(event):
    event_dict = {}
    event_dict['venue_id'] = event.venue_id
    event_dict['title'] = event.title
    event_dict['event_date'] = get_timestamp(event.event_date)     
    event_dict['description'] = event.event_description
    event_dict['creation_date'] = get_timestamp(event.creation_date)
    event_dict['organizer'] = user_to_dict(event.organizer)

    return event_dict


def comment_to_dict(comment):
    comment_dict = {}
    comment_dict['user'] = user_to_dict(comment.user)
    comment_dict['comment'] = comment.comment
    comment_dict['creation_date'] = get_timestamp(comment.creation_date)
    return comment_dict 


def attendance_to_dict(attendance):
    attendee_dict = {}
    attendee_dict['user'] = user_to_dict(attendance.user)
    attendee_dict['attendance_status'] = attendance.attendance
    return attendee_dict 
