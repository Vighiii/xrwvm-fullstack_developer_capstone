from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Car Model
class CarModel(models.Model):

    CAR_TYPES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
        ('Hatchback', 'Hatchback'),
        ('Truck', 'Truck'),
        ('Coupe', 'Coupe'),
    )

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='car_models'
    )

    name = models.CharField(max_length=100)

    dealer_id = models.IntegerField(null=True, blank=True)

    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default='Sedan'
    )

    year = models.IntegerField(
        default=now().year,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"