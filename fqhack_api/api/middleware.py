"""Middlewares for the api app."""

import traceback

from api import utils


class RequestUserInformationMiddleware:
    def process_request(self, request):
        if request.method == 'POST':
            query_dict = request.POST
        elif request.method == 'GET':
            query_dict = request.GET
        else:
            return None

        request.user_id = query_dict.get('user_id')
        return None
 

class ErrorLoggerMiddleware:
    def process_exception(self, request, exception):
        tb = traceback.format_exc()
        utils.log('API Exception: %s: %s' % (exception, tb)) 
