from django.contrib import admin
from models import Crime, Offense, Category

# Register your models here.
admin.site.register(Crime)

admin.site.register(Category)

class OffenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category')
    list_editable = ('category')
    ordering = ('name', 'category')

admin.site.register(Offense, OffenseAdmin)