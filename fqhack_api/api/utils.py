import time

from api import models


def validate_args(args):
    """Returns True or False based on whether all args were provided."""
    # Check if all required args are provided.
    args_list = [event_id, user_id, comment]
    filtered_args = filter(None, args_list)
    return len(args_list) != len(filtered_args)


def event_to_dict(event):
    # Note that the datetime objects are converted to timestamp
    event_dict = {}
    event_dict['venue_id'] = event.venue_id
    event_dict['title'] = event.title
    event_dict['event_date'] = time.mktime(
            event.event_date.timetuple())
    event_dict['description'] = event.event_description
    event_dict['creation_date'] = time.mktime(
            event.creation_date.timetuple())
    # add organizer to the event content

    return event_dict


def comment_to_dict(comment):
    # Note that the datetime objects are converted to timestamp
    comment_dict= {}

    return comment_dict 
