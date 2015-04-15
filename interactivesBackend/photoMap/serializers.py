from rest_framework import serializers
from photoMap.models import Map, Event
import string

class EventLimitedSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('id', 'latitude', 'longitude', 'name', 'date', 'image', 'endDate')

class MapSerializer(serializers.ModelSerializer):
	events = EventLimitedSerializer(many=True, read_only=True)

	class Meta:
		model = Map
		fields = ('id', 'name', 'event_type', 'events', 'default_image')

class EventSerializer(serializers.ModelSerializer):
	description = serializers.SerializerMethodField()

	class Meta:
		model = Event
		fields = ('id', 'latitude', 'longitude', 'name', 'description', 'date', 'image', 'endDate', 'eventLink')

	def get_description(self, obj):
		return string.replace('\n', obj.description, '<br>')