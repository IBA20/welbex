from django.contrib import admin

from .models import Location, Shipment, Car


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    readonly_fields = ('zip', 'city', 'state', 'lat', 'lon',)
    list_display = ('zip', 'city', 'state', 'lat', 'lon')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'pick_up', 'delivery', 'weight',)
    raw_id_fields = ('pick_up', 'delivery',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('number', 'location', 'carrying',)
    raw_id_fields = ('location',)
    ordering = ('number',)
