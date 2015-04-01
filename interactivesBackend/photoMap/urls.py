from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from photoMap import views

urlpatterns = (
    url(r'^(?P<map_id>\d+)/$', views.map, name='map'),
	url(r'^api/maps/(?P<pk>[0-9]+)/$', views.MapDetail.as_view(), name='mapAPIListing'), 
	url(r'^api/events/(?P<pk>[0-9]+)/$', views.EventDetail.as_view()),
	url(r'^api/subevents/(?P<pk>[0-9]+)/$', views.SubEventDetail.as_view()),
)