from django.shortcuts import render

from models import Crime, Offense
from serializers import CrimeDetailSerializer, CrimeListSerializer, OffenseListSerializer

from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Polygon

import pytz
import datetime
from dateutil.parser import parse

# Create your views here.
class OffenseList(generics.ListAPIView):
    queryset = Offense.objects.all()
    serializer_class = OffenseListSerializer

class CrimeDetail(generics.RetrieveAPIView):
    queryset = Crime.objects.all().prefetch_related('offenses')
    serializer_class = CrimeDetailSerializer

class CrimeList(generics.ListAPIView):
    def get_queryset(self):
        MAX_ALLOWED_DAYS = datetime.timedelta(days=7)

        queryset = Crime.objects.all().prefetch_related('offenses')
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
            offenseTimeRange[0] = timezone.localize(datetime.datetime.today() - MAX_ALLOWED_DAYS)
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])

        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
        if offenseTimeRange[1] and ((offenseTimeRange[1] - offenseTimeRange[0]) <= MAX_ALLOWED_DAYS):
            queryset = queryset.filter(offense_time__lte=offenseTimeRange[1])
        else:
            queryset = queryset.filter(offense_time__lte=offenseTimeRange[0] + MAX_ALLOWED_DAYS)

        if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
            geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                    bbTopRightX, bbTopRightY))
            queryset = queryset.filter(geocode_location__within=geom)

        if offense:
            queryset = queryset.filter(offenses__pk=offense)

        return queryset

    serializer_class = CrimeListSerializer

class CrimeCount(APIView):
    """
    A view that returns the count of active users.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        queryset = Crime.objects.all()
        
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

        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lte=offenseTimeRange[1])

        if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
            geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                    bbTopRightX, bbTopRightY))
            queryset = queryset.filter(geocode_location__within=geom)

        if offense:
            queryset = queryset.filter(offenses__pk=offense)



        content = {'number':queryset.count()}
        return Response(content)
