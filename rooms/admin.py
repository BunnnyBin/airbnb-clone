from django.contrib import admin
from . import models

@admin.register(models.RoomType, models.HouseRule, models.Facility, models.Amenity)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
