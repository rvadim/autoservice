from django.contrib import admin
from station.models import *


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_cost', 'max_cost', 'min_duration',
                    'max_duration')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date_time', 'approved', 'completed')
