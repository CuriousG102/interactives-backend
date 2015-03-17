from django.shortcuts import render

from models import Crime
from serializers import CrimeDetailSerializer, CrimeSerializer

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

class Crime(generics.ListAPIView):
	def get_queryset(self):
		MAX_ALLOWED_DAYS = datetime.timedelta(days=7)

		queryset = Crime.objects.all()
		offenseTimeRange = [self.GET.get('offenseStartRange', None),
							self.GET.get('offenseEndRange', None)]
		bbBottomLeftX = self.GET.get('bbBottomLeftX', None)
		bbBottomLeftY = self.GET.get('bbBottomLeftY', None)
		bbTopRightX = self.GET.get('bbTopRightX', None)
		bbTopRightY = self.GET.get('bbTopRightY', None)
		offense = self.GET.get('offense', None)

		if offenseTimeRange[0]:
			offenseTimeRange[0] = parse(offenseTimeRange[0])
			queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
		else:
			timezone = pytz.timezone('US/Central')
			queryset = queryset.filter(offense_time__gte=timezone.localize(datetime.today() - datetime.timedelta(days=7)))


		if offenseTimeRange[1]:
			offenseTimeRange[1] = parse(offenseTimeRange[1])
		if offenseTimeRange[1] and ((offenseTimeRange[1] - offenseTimeRange[0]) <= MAX_ALLOWED_DAYS):
			queryset = queryset.filter(offense_time__lte=offenseTimeRange[1])
		else:
			queryset = queryset.filter(offense_time__lte=timezone.localize(datetime.today()))

		if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
			geom = Polygon.frombbox(bbBottomLeftX, bbBottomLeftY, 
									bbTopRightX, bbTopRightY)
			queryset = queryset.filter(geocode_location__within=geom)

		if offense:
			queryset = queryset.filter(offense__name__exact=offense)

		return queryset

	serializer_class = CrimeSerializer


