from django.contrib import admin
from api import models 

admin.site.register(models.APIUser)
admin.site.register(models.Event)
admin.site.register(models.Comment)
admin.site.register(models.Attendance)
