from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
# Use TabularInline for related models
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of extra inline forms


# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("name", "car_make", "type", "year", "dealer_id")
    # Enable search fields
    search_fields = ("name", "car_make")
    # Filters for easy access
    list_filter = ("type", "year", "car_make")
    # Order by brand then model name
    ordering = ("car_make", "name")


# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    # Fields to display: brand name and description
    list_display = ("name", "description")
    # Search brands by name
    search_fields = ("name",)
    # Sort brands alphabetically
    ordering = ("name",)
    # Show related CarModels inline
    inlines = [CarModelInline]


# Register models here
# admin.site.register(CarMake)
# admin.site.register(CarModel)
