from django.core.exceptions import ValidationError
from django.db import models

def validate_latitude(latitude):
	if latitude < -90.0 or latitude > 90.0:
		raise ValidationError(u'%s is not a valid latitude' % latitude)

def validate_longitude(longitude):
	if longitude < -180.0 or longitude > 180.0:
		raise ValidationError(u'%s is not a valid longitude' % longitude)


# Create your models here.
class Map(models.Model):
	name = models.CharField(max_length=50)
	event_type = models.CharField(max_length=20)
	subevent_type = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Event(models.Model):
	map = models.ForeignKey(Map, related_name='events')
	latitude = models.FloatField(validators=[validate_latitude])
	longitude = models.FloatField(validators=[validate_longitude])
	name = models.CharField(max_length=80)
	description = models.TextField(null=True, blank=True)
	date = models.DateField()
	endDate = models.DateField()
	image = models.ImageField(upload_to='photoMap',
		                      null=True, blank=True)

	def __unicode__(self):
		return self.name

class SubEvent(models.Model):
	event = models.ForeignKey(Event, related_name='subevents')
	name = models.CharField(max_length=80)
	description = models.TextField()
	time = models.DateTimeField(null=True, blank=True)
	image = models.ImageField(upload_to = 'photoMap',
							  null=True, blank=True)

	def __unicode__(self):
		return self.name