from django.contrib import admin
from .models import CarMake, CarModel

# Optional: Inline admin for CarModel within CarMake view
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# CarMake Admin with inline CarModel
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')

# CarModel Admin
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ('type', 'year', 'car_make')
    search_fields = ('name',)

# Register models with admin
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
