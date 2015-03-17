from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from crimeAPI import views

urlpatterns = (
	url(r'^crime/(?P<pk>[0-9]+)/$', views.CrimeDetail.as_view()),
	url(r'^crime/$', views.CrimeList.as_view()),
	url(r'^count/$', view.CrimeCount.as_view()),
)