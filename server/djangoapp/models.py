from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator



class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  



class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Establishes Many-to-One relationship
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()  # Refers to a dealer in another database (e.g., Cloudant)

    # Car types with limited choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more types if needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    
    # Year of manufacture with validators
    year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.now().year),
            MinValueValidator(1980)
        ],
        default=datetime.now().year
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"