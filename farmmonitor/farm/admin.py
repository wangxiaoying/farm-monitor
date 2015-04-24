from django.contrib import admin
from farm.models import *
# Register your models here.

class NetworkTestAdmin(admin.ModelAdmin):
	list_display = ('id', 'message', 'photo')

class SampleAdmin(admin.ModelAdmin):
	list_display = ('id', 'longtitude', 'latitude', 'moisture', 'air_temp', 'leave_temp', 'humidity', 'transpiration', 'photo', 'time')

admin.site.register(NetworkTest, NetworkTestAdmin)
admin.site.register(Sample, SampleAdmin)