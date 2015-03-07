from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.
from photoMap.models import Map, Event, SubEvent

class SubEventInline(NestedStackedInline):
	model = SubEvent
	extra = 1
	fk_name = 'event'

class EventInline(NestedStackedInline):
	model = Event
	extra = 1
	fk_name = 'map'
	inlines = [SubEventInline]

class MapAdmin(NestedModelAdmin):
	model = Map
	inlines = [EventInline]

admin.site.register(Map, MapAdmin)