from django.contrib.gis.db import models

# Create your models here.
class Crime(models.Model):
	report_number = models.CharField(max_length=50, null=True, db_index=True)
	report_time = models.DateTimeField(null=True, db_index=True)
	offense_time = models.DateTimeField(null=True, db_index=True)
	offenses = models.ManyToManyField('Offense', db_index=True)
	offense_address = models.CharField(max_length=100, null=True, db_index=True)
	offense_census_tract = models.CharField(max_length=20, null=True, db_index=True)
	offense_district = models.CharField(max_length=5, null=True, db_index=True)
	offense_area_command = models.CharField(max_length=50, null=True, db_index=True)
	offense_investigator_assigned = models.CharField(max_length=50, null=True, db_index=True)
	geocoded = models.BooleanField(default=False, db_index=True)
	geocode_location = models.PointField(null=True, db_index=True)

class Offense(models.Model):
	name = models.CharField(max_length=80)

	def __unicode__(self):
		return self.name