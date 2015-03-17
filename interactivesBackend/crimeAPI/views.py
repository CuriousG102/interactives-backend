from django.shortcuts import render

from models import Crime
from serializers import CrimeDetailSerializer, CrimeListSerializer

from django.shortcuts import render
from rest_framework import generics
from django.contrib.gis.geos import Polygon

import pytz
import datetime
from dateutil.parser import parse

# Create your views here.
class CrimeDetail(generics.RetrieveAPIView):
	queryset = Crime.objects.all()
	serializer_class = CrimeDetailSerializer

class CrimeList(generics.ListAPIView):
	def get_queryset(self):
		MAX_ALLOWED_DAYS = datetime.timedelta(days=7)

		queryset = Crime.objects.all()
		offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
							self.request.QUERY_PARAMS.get('offenseEndRange', None)]
		bbBottomLeftX = self.request.QUERY_PARAMS.get('bbBottomLeftX', None)
		bbBottomLeftY = self.request.QUERY_PARAMS.get('bbBottomLeftY', None)
		bbTopRightX = self.request.QUERY_PARAMS.get('bbTopRightX', None)
		bbTopRightY = self.request.QUERY_PARAMS.get('bbTopRightY', None)
		offense = self.request.QUERY_PARAMS.get('offense', None)

		timezone = pytz.timezone('US/Central')
		if offenseTimeRange[0]:
			offenseTimeRange[0] = parse(offenseTimeRange[0])
			queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
		else:
			
			queryset = queryset.filter(offense_time__gte=timezone.localize(datetime.datetime.today() - MAX_ALLOWED_DAYS))

		if offenseTimeRange[1]:
			offenseTimeRange[1] = parse(offenseTimeRange[1])
		if offenseTimeRange[1] and ((offenseTimeRange[1] - offenseTimeRange[0]) <= MAX_ALLOWED_DAYS):
			queryset = queryset.filter(offense_time__lte=offenseTimeRange[1])
		else:
			queryset = queryset.filter(offense_time__lte=timezone.localize(datetime.datetime.today()))

		if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
			geom = Polygon.frombbox(bbBottomLeftX, bbBottomLeftY, 
									bbTopRightX, bbTopRightY)
			queryset = queryset.filter(geocode_location__within=geom)

		if offense:
			queryset = queryset.filter(offense__name__exact=offense)

		return queryset

	serializer_class = CrimeListSerializer


