from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    """
    CarMake model representing car manufacturers
    """
    name = models.CharField(max_length=100, help_text='Enter a car make (e.g. BMW, Mercedes, Toyota)')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the car make')
    
    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
    CarModel model representing specific car models
    """
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
        ('COUPE', 'Coupe'),
        ('PICKUP', 'Pickup'),
    ]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Enter a car model name')
    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default='SEDAN',
        help_text='Select car type'
    )
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
        help_text='Enter model year (2015-2023)'
    )
    
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
