from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1  # Number of empty forms to display for add new related objects
    fields = ('name', 'type', 'year')


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'car_make')


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'established_year')
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
