from django.contrib import admin
from .models import CarMake, CarModel


# Register CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# Register CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'car_type', 'year')


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
