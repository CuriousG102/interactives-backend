from django.shortcuts import render

from models import Map, Event, SubEvent
from serializers import MapSerializer, EventSerializer, SubEventSerializer
from rest_framework import generics

# Create your views here.
class MapDetail(generics.RetrieveAPIView):
	queryset = Map.objects.all().prefetch_related('events')
	serializer_class = MapSerializer

class EventDetail(generics.RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer

class SubEventDetail(generics.RetrieveAPIView):
	queryset = SubEvent.objects.all()
	serializer_class = SubEventSerializer