# Uncomment the following imports before adding the Model code

from django.db import models


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon')
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES,
                            default='SUV')
    year = models.IntegerField(default=2023)

    def __str__(self):
        return self.name  # Return the name as the string representation
