from django.contrib import admin
from .models import Region, Craft, Master, Booking, Profile

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "craft_type",
        "region",
        "latitude",
        "longitude",
        "language",
        "schedule",
        "price",
        "experience",
        "craft_category",
    )
    list_filter = ("craft_type", "region", "language", "schedule")
    search_fields = ("name", "description", "language", "schedule", "craft_category")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("name", "craft", "phone", "email")
    search_fields = ("name", "craft__name")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("craft", "name", "email", "phone", "created_at")
    list_filter = ("craft", "created_at")
    search_fields = ("name", "email", "phone", "message")
    ordering = ("-created_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)
