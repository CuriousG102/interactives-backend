from rest_framework import serializers
from crimeAPI.models import Crime


class CrimeDetailSerializer(serializers.ModelSerializer):
	longitude = serializers.SerializerMethodField()
	latitude = serializers.SerializerMethodField()

	class Meta:
		model = Crime
		fields = ('id', 'report_number', 'report_time', 'offense_time', 'offenses', 'offense_address', 'offense_census_tract', 'offense_district', 'offense_area_command', 'offense_investigator_assigned', 'geocoded', 'longitude', 'latitude')
		depth=1

	def get_longitude(self, obj):
		if obj.geocode_location:
			return obj.geocode_location.x
		else:
			return 0.0

	def get_latitude(self, obj):
		if obj.geocode_location:
			return obj.geocode_location.y
		else:
			return 0.0

class CrimeListSerializer(serializers.ModelSerializer):
	longitude = serializers.SerializerMethodField()
	latitude = serializers.SerializerMethodField()

	class Meta:
		model = Crime
		fields = ('id', 'report_time', 'offense_time', 'offense_district', 'offense_area_command', 'geocoded', 'longitude', 'latitude', 'offenses')

	def get_longitude(self, obj):
		if obj.geocode_location:
			return obj.geocode_location.x
		else:
			return 0.0

	def get_latitude(self, obj):
		if obj.geocode_location:
			return obj.geocode_location.y
		else:
			return 0.0