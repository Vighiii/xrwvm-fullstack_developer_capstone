from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Car Model model
class CarModel(models.Model):
    # Many-to-One relationship (one CarMake has many CarModels)
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]

    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV',
    )

    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015),
        ],
    )

    def __str__(self):
        return self.name
