from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# CarModelAdmin class


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'year', 'car_make', 'dealer_id')
    list_filter = ('car_type', 'year', 'car_make')
    search_fields = ('name', 'year', 'car_make__name', 'dealer_id', 'car_type')

# CarMakeAdmin class with CarModelInline


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
