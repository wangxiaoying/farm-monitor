from django.contrib import admin
from farm.models import *
# Register your models here.

class NetworkTestAdmin(admin.ModelAdmin):
	list_display = ('id', 'message', 'photo')

admin.site.register(NetworkTest, NetworkTestAdmin)