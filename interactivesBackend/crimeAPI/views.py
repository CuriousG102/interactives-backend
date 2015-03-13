from django.shortcuts import render

from models import Crime
from serializers import CrimeSerializer


from django.shortcuts import render

from models import Map, Event, SubEvent
from serializers import MapSerializer, EventSerializer, SubEventSerializer
from rest_framework import generics
# Create your views here.
class CrimeDetail(generics.RetrieveAPIView):
	queryset = Crime.objects.all()
	serializer_class = CrimeSerializer