from django.contrib import admin
from . import models

@admin.register(models.RoomType, models.HouseRule, models.Facility, models.Amenity)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    fieldsets = (
        (
        "Basic Info",
        {"fields": ("name","description","country","address","price")}
        ),
        (
            "Times",
            {"fields": ("check_in","check_out","instant_book")}
        ),
        (
            "Space",
            {"fields": ("guests", "beds", "bedrooms", "baths")}
        ),
        (
            "More About the Space",
            {"classes" : ('collapse',),
             "fields":("amenities","facilities","house_rules")}
        ),
        (
            "Last Details",
            {"fields":("host",)}
        ),
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("city", "host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
