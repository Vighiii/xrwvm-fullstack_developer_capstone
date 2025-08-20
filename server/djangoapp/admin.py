from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):  
    model = CarModel 
    extra = 1 

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'type', 'year') 
    search_fields = ['name', 'car_make__name'] 

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founding_year', 'website') 
    search_fields = ['name', 'country']  
    inlines = [CarModelInline] 

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)