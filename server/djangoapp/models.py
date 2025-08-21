from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Optional additional fields
    country = models.CharField(max_length=100, default="Unknown", blank=True)
    founded_year = models.IntegerField(
        default=1900,
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(datetime.now().year),
        ],
    )

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('TRUCK', 'Truck'),
        ('CONVERTIBLE', 'Convertible'),
    ]

    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(
        default=datetime.now().year,
        validators=[
            MinValueValidator(1990),
            MaxValueValidator(datetime.now().year),
        ],
    )
    dealer_id = models.IntegerField()  # Refers to a dealer in Cloudant DB

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
