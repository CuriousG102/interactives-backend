from rest_framework import serializers
from photoMap.models import Map, Event, SubEvent

class MapSerializer(serializers.ModelSerializer):
	events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Map
		fields = ('id', 'name', 'event_type', 'subevent_type', 'events')

class EventSerializer(serializers.ModelSerializer):
	subevents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Event
		fields = ('id', 'latitude', 'longitude', 'name', 'description', 'date', 'image', 'subevents', 'endDate')

class SubEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubEvent
		fields = ('id', 'name', 'description', 'time', 'image')