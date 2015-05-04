from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from crimeAPI import views

urlpatterns = (
	url(r'^crime/(?P<pk>[0-9]+)/$', views.CrimeDetail.as_view()),
	url(r'^crime/$', views.CrimeList.as_view()),
	url(r'^count/$', views.CrimeCount.as_view()),
    url(r'^countincrement/$', views.CrimeCountIncrement.as_view()),
    url(r'^offense/$', views.OffenseList.as_view()),
    url(r'^category/$', views.CategoryList.as_view()),
    url(r'^district/$', views.CensusDistrictCrimeCount.as_view()),
    url(r'^countArea/$', views.CrimeCountByArea.as_view()),
    url(r'^timeToReport/$', views.OffenseVReportTime.as_view()),
)