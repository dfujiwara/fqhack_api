from django.conf.urls import patterns, include, url

from api import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fqhack_api.views.home', name='home'),
    # url(r'^fqhack_api/', include('fqhack_api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^healthz/', views.healthz),

    # Class based views.
    url(r'^events/', views.EventsView.as_view()),
    url(r'^event/(\d+)/$', views.EventView.as_view()),
    url(r'^event/(\d+)/comment/$', views.CommentView.as_view()),
    url(r'^event/(\d+)/attendance/$', views.AttendanceView.as_view()),

    # Class based views with foursquare interaction
    url(r'^venues/$', views.VenuesView.as_view()),
)
