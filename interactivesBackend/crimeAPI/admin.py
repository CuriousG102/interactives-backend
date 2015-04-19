from django.contrib import admin
from models import Crime, Offense, Category

# Register your models here.
admin.site.register(Crime)
admin.site.register(Offense)
admin.site.register(Category)