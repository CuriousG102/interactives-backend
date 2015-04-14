from django.shortcuts import render
from django.http import Http404
from django.views.decorators.http import require_http_methods

from models import Map, Event
from serializers import MapSerializer, EventSerializer
from rest_framework import generics

# Create your views here.
class MapDetail(generics.RetrieveAPIView):
	queryset = Map.objects.all().prefetch_related('events')
	serializer_class = MapSerializer

class EventDetail(generics.RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer

@require_http_methods(["GET"])
def map(request, map_id):
    try:
        map = Map.objects.get(pk=map_id)
    except Map.DoesNotExist:
        raise Http404("Map does not exist")
    return render(request, 'photoMap/detail.html', {'map':map})