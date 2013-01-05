# Create your views here.

from django.http import HttpResponse

def healthz(request):
    return HttpResponse("Ok")
