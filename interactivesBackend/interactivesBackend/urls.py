from django.conf.urls import patterns, include, url
from django.contrib import admin

import photoMap

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'interactivesBackend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^photoMap/', include('photoMap.urls',
    						   namespace='photoMap')),
    url(r'^crimeAPI/', include('crimeAPI.urls',
    						   namespace='crimeAPI')),
    url(r'^api-auth/', include('rest_framework.urls',
   							   namespace='rest_framework')),
)
