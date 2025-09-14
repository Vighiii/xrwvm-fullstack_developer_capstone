from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    CAR_BRAND = [
        ('TOYOTA', 'Toyota'),
        ('HONDA', 'Honda'),
        ('HYUNDAI', 'Hyundai'),
        ('FORD', 'Ford'),
        ('CHEVROLET', 'Chevrolet'),
        ('MITSUBISHI', 'Mitsubishi'),
    ]
    brand = models.CharField(max_length=10, 
                             choices=CAR_BRAND, default='TOYOTA')

    def __str__(self):
        return self.name  

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('CAMRY', 'Camry'),
        ('CIVIC', 'Civic')
    ]
    type = models.CharField(max_length=10, 
                            choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
                               validators=[
                                   MaxValueValidator(2023), 
                                   MinValueValidator(2015)
                               ])

    def __str__(self):
        return self.name