import datetime
import requests
import time

from django.conf import settings

from api import models

def log(log_message):
    print(log_message)


def get_timestamp(dt):
    return time.mktime(dt.timetuple())


def get_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp) 


def validate_args(arg_list):
    """Returns True or False based on whether all args were provided."""
    # Check if all required args are provided.
    filtered_arg_list = filter(None, arg_list)
    return len(arg_list) != len(filtered_arg_list)


def user_to_dict(user):
    user_dict = {}
    user_dict['id'] = user.id
    user_dict['name'] = user.full_name()
    return user_dict    


def event_to_dict(event):
    event_dict = {}
    event_dict['title'] = event.title
    event_dict['event_date'] = get_timestamp(event.event_date)     
    event_dict['description'] = event.event_description
    event_dict['creation_date'] = get_timestamp(event.creation_date)
    event_dict['organizer'] = user_to_dict(event.organizer)

    # Get venue details.
    # Must handle status_code eventually.
    url = 'https://api.foursquare.com/v2/venues/%s' % event.venue_id
    params = {}
    params['client_id'] = settings.CLIENT_ID
    params['client_secret'] = settings.CLIENT_SECRET 

    fq_response = requests.get(url, params=params)
    json_response = fq_response.json()['response']
    venue_content = venue_to_dict(json_response['venue'])
    event_dict['venue'] = venue_content

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


def venue_to_dict(venue):
    # Note that incoming param venue is already a json structured object;
    # This function basically filters out information selectively.
    venue_dict = {}
    venue_dict['id'] = venue['id']
    venue_dict['name'] = venue['name']
    venue_dict['location'] = venue['location']
    return venue_dict
