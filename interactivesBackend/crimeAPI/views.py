from django.shortcuts import render

from models import Crime, Offense, Category
from serializers import CrimeDetailSerializer, CrimeListSerializer, OffenseListSerializer, CategoryListSerializer

from django.http import Http404
from django.db.models import Count, Avg
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_jsonp.renderers import JSONPRenderer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Polygon

import datetime
from dateutil.parser import parse
from pytz import timezone

# Create your views here.
class CategoryList(generics.ListAPIView):
    """
    Crime offense codes have been placed into categories. Those categories are listed at this API
    endpoint
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class OffenseList(generics.ListAPIView):
    """
    This endpoint lists all offenses available via this API
    """
    queryset = Offense.objects.all()
    serializer_class = OffenseListSerializer

class CrimeDetail(generics.RetrieveAPIView):
    """
    This will list the minute details of a specific crime requested by PK
    """
    queryset = Crime.objects.all().prefetch_related('offenses')
    serializer_class = CrimeDetailSerializer

class CrimeList(generics.ListAPIView):
    """
    Endpoint that lists crimes. The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    bbBottomLeftX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbBottomLeftY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    offense -- Number, pk of offense you wish to filter crimes by
    census -- Decimal number, district you want crimes in
    category -- Number, pk of category you wish to filter crimes by 
    """
    def get_queryset(self):
        MAX_ALLOWED_DAYS = datetime.timedelta(days=7)

        queryset = Crime.objects.all().prefetch_related('offenses').prefetch_related('offenses__category')
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        bbBottomLeftX = self.request.QUERY_PARAMS.get('bbBottomLeftX', None)
        bbBottomLeftY = self.request.QUERY_PARAMS.get('bbBottomLeftY', None)
        bbTopRightX = self.request.QUERY_PARAMS.get('bbTopRightX', None)
        bbTopRightY = self.request.QUERY_PARAMS.get('bbTopRightY', None)
        offense = self.request.QUERY_PARAMS.get('offense', None)
        census = self.request.QUERY_PARAMS.get('census', None)
        category = self.request.QUERY_PARAMS.get('category', None)

        if offenseTimeRange[0]:
            offenseTimeRange[0] = parse(offenseTimeRange[0])
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
        # else:
        #     central = timezone('US/Central')
        #     offenseTimeRange[0] = central.localize(datetime.datetime.today() - MAX_ALLOWED_DAYS)
        
        # queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])

        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[1])
        # if offenseTimeRange[1] and ((offenseTimeRange[1] - offenseTimeRange[0]) <= MAX_ALLOWED_DAYS):
        #     queryset = queryset.filter(offense_time__lte=offenseTimeRange[1])
        # else:
        #     queryset = queryset.filter(offense_time__lte=offenseTimeRange[0] + MAX_ALLOWED_DAYS)

        if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
            geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                    bbTopRightX, bbTopRightY))
            queryset = queryset.filter(geocode_location__within=geom)

        if offense:
            queryset = queryset.filter(offenses__pk=offense)

        if category:
            queryset = queryset.filter(offenses__category__pk=category)

        if census:
            queryset = queryset.filter(offense_census_tract=census)

        return queryset

    serializer_class = CrimeListSerializer

class CrimeCountIncrement(APIView):
    """
    Endpoint that returns the count of crimes fulfilling the criteria given in the query
    in hour increments specified by the query

    Content looks like this: [{'number':queryset.count()}, ...]
    Please filter by offenseStartRange and offenseEndRange or I will have to throttle this endpoint

    increment -- Number of hours for each increment

    The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    bbBottomLeftX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbBottomLeftY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    offense -- Number, pk of offense you wish to filter crimes by
    census -- Decimal number, district you want crimes in
    category -- Number, pk of category you wish to filter crimes by
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, JSONPRenderer)

    def get(self, request, format=None):
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        bbBottomLeftX = self.request.QUERY_PARAMS.get('bbBottomLeftX', None)
        bbBottomLeftY = self.request.QUERY_PARAMS.get('bbBottomLeftY', None)
        bbTopRightX = self.request.QUERY_PARAMS.get('bbTopRightX', None)
        bbTopRightY = self.request.QUERY_PARAMS.get('bbTopRightY', None)
        offense = self.request.QUERY_PARAMS.get('offense', None)
        census = self.request.QUERY_PARAMS.get('census', None)
        category = self.request.QUERY_PARAMS.get('category', None)
        increment = self.request.QUERY_PARAMS.get('increment', None)

        # if (not increment) or (not offenseTimeRange[0]) or (not offenseTimeRange[1]):
        #     return Http404('<h1>You need an increment and times dummy</h1>')

        offenseTimeRange[0] = parse(offenseTimeRange[0])
        offenseTimeRange[1] = parse(offenseTimeRange[1])

        # content = [{'number':queryset.count()}, ...]
        content = []
        increment = datetime.timedelta(hours=int(increment))
        while (offenseTimeRange[0] + increment) <= offenseTimeRange[1]:
            queryset = Crime.objects.all()
            if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
                geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                        bbTopRightX, bbTopRightY))
                queryset = queryset.filter(geocode_location__within=geom)

            if offense:
                queryset = queryset.filter(offenses__pk=offense)

            if category:
                queryset = queryset.filter(offenses__category__pk=category)

            if census:
                queryset = queryset.filter(offense_census_tract=census)
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[0] + increment)
            content.append({'number':queryset.count()})
            offenseTimeRange[0] += increment

        
        return Response(content)



class CrimeCount(APIView):
    """
    A view that returns the count of crimes fulfilling the criteria given in the query.

    The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    bbBottomLeftX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbBottomLeftY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    offense -- Number, pk of offense you wish to filter crimes by
    census -- Decimal number, district you want crimes in
    category -- Number, pk of category you wish to filter crimes by
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, JSONPRenderer)

    def get(self, request, format=None):
        queryset = Crime.objects.all()
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        bbBottomLeftX = self.request.QUERY_PARAMS.get('bbBottomLeftX', None)
        bbBottomLeftY = self.request.QUERY_PARAMS.get('bbBottomLeftY', None)
        bbTopRightX = self.request.QUERY_PARAMS.get('bbTopRightX', None)
        bbTopRightY = self.request.QUERY_PARAMS.get('bbTopRightY', None)
        offense = self.request.QUERY_PARAMS.get('offense', None)
        census = self.request.QUERY_PARAMS.get('census', None)
        category = self.request.QUERY_PARAMS.get('category', None)

        if offenseTimeRange[0]:
            offenseTimeRange[0] = parse(offenseTimeRange[0])
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])

        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[1])

        if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
            geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                    bbTopRightX, bbTopRightY))
            queryset = queryset.filter(geocode_location__within=geom)

        if offense:
            queryset = queryset.filter(offenses__pk=offense)

        if category:
            queryset = queryset.filter(offenses__category__pk=category)

        if census:
            queryset = queryset.filter(offense_census_tract=census)

        content = {'number':queryset.count()}
        return Response(content)

class CensusDistrictCrimeCount(APIView):
    """
    Count of number of crimes for each district

    The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    offense -- Number, pk of offense you wish to filter crimes by
    category -- Number, pk of category you wish to filter crimes by
    """

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, JSONPRenderer)

    def get(self, request, format=None):
        queryset = Crime.objects.all()
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        offense = self.request.QUERY_PARAMS.get('offense', None)
        category = self.request.QUERY_PARAMS.get('category', None)

        if offenseTimeRange[0]:
            offenseTimeRange[0] = parse(offenseTimeRange[0])
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[1])
        if offense:
            queryset = queryset.filter(offenses__pk=offense)
        if category:
            queryset = queryset.filter(offenses__category__pk=category)

        content = queryset.values('offense_census_tract').annotate(count=Count('offense_census_tract'))
        return Response(content)

class OffenseVReportTime(APIView):
    """
    Average of the difference between when an offense was thought to have occurred and when that offense
    was reported. Lists by APD area command.

    The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    bbBottomLeftX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbBottomLeftY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightX -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    bbTopRightY -- One of four coordinate parameters for filtering crimes by their presence in a bounding box
    offense -- Number, pk of offense you wish to filter crimes by
    census -- Decimal number, district you want crimes in
    category -- Number, pk of category you wish to filter crimes by
    """

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, JSONPRenderer)

    def get(self, request, format=None):
        queryset = Crime.objects.all()
        queryset = Crime.objects.all()
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        bbBottomLeftX = self.request.QUERY_PARAMS.get('bbBottomLeftX', None)
        bbBottomLeftY = self.request.QUERY_PARAMS.get('bbBottomLeftY', None)
        bbTopRightX = self.request.QUERY_PARAMS.get('bbTopRightX', None)
        bbTopRightY = self.request.QUERY_PARAMS.get('bbTopRightY', None)
        offense = self.request.QUERY_PARAMS.get('offense', None)
        census = self.request.QUERY_PARAMS.get('census', None)
        category = self.request.QUERY_PARAMS.get('category', None)

        if offenseTimeRange[0]:
            offenseTimeRange[0] = parse(offenseTimeRange[0])
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])

        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[1])

        if bbTopRightY and bbTopRightX and bbBottomLeftY and bbBottomLeftX:
            geom = Polygon.from_bbox((bbBottomLeftX, bbBottomLeftY, 
                                    bbTopRightX, bbTopRightY))
            queryset = queryset.filter(geocode_location__within=geom)

        if offense:
            queryset = queryset.filter(offenses__pk=offense)

        if category:
            queryset = queryset.filter(offenses__category__pk=category)

        if census:
            queryset = queryset.filter(offense_census_tract=census)

        # there's definitely room for optimization in the following algorithm
        areas = queryset.values('offense_area_command').distinct()
        avgDict = {}
        for area in areas:
            filterString = area['offense_area_command']
            avgDict[filterString] = queryset.filter(offense_area_command=filterString).aggregate(Avg('time_to_report_in_seconds'))
            avgDict[filterString] = avgDict[filterString]['time_to_report_in_seconds__avg']

        return Response(avgDict)

class CrimeCountByArea(APIView):
    """
    Count of number of crimes for each Area Command of APD. 

    The responses generated via this endpoint can be filtered by adding various parameters
    offenseStartRange -- ISO 8601, enter a date/time and only get crimes that occurred after it
    offenseEndRange -- ISO 8601, enter a date/time and only get crimes that occured before it
    offense -- Number, pk of offense you wish to filter crimes by
    category -- Number, pk of category you wish to filter crimes by
    """

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, JSONPRenderer)
    def get(self, request, format=None):
        queryset = Crime.objects.all()
        offenseTimeRange = [self.request.QUERY_PARAMS.get('offenseStartRange', None),
                            self.request.QUERY_PARAMS.get('offenseEndRange', None)]
        offense = self.request.QUERY_PARAMS.get('offense', None)
        category = self.request.QUERY_PARAMS.get('category', None)

        if offenseTimeRange[0]:
            offenseTimeRange[0] = parse(offenseTimeRange[0])
            queryset = queryset.filter(offense_time__gte=offenseTimeRange[0])
        if offenseTimeRange[1]:
            offenseTimeRange[1] = parse(offenseTimeRange[1])
            queryset = queryset.filter(offense_time__lt=offenseTimeRange[1])
        if offense:
            queryset = queryset.filter(offenses__pk=offense)
        if category:
            queryset = queryset.filter(offenses__category__pk=category)

        # there's definitely room for optimization in the following algorithm
        areas = queryset.values('offense_area_command').distinct()
        countDict = {}
        for area in areas:
            count = queryset.filter(offense_area_command=area['offense_area_command']).count()
            countDict[area['offense_area_command']] = count

        return Response(countDict)

def crimeMap(request):
    catOffenseNames = []
    for category in Category.objects.all().order_by('name'):
        catOffenseName = (category, 
                          Offense.objects.all().filter(category=category).order_by('name'))
        catOffenseNames.append(catOffenseName)
    nullCatOffenseNames = Offense.objects.all().filter(category__isnull=True).order_by('name')
    return render(request, 'crimeAPI/index.html', 
                  {'nullCatOffenseNames':nullCatOffenseNames,
                  'catOffenseNames':catOffenseNames})

def baseView(request):
    raise Http404("Poll does not exist")