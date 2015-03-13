from django.contrib import admin
from models import Crime, Offense

# Register your models here.
admin.site.register(Crime, Offense)