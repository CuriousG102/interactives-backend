from rest_framework import serializers
from crimeAPI.models import Crime


class CrimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Crime
		fields = ('report_number', 'report_time', 'offense_time', 'offenses', 'offense_address', 'offense_census_tract', 'offense_district', 'offense_area_command', 'offense_investigator_assigned', 'geocoded')