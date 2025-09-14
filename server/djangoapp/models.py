# Uncomment the following imports before adding the Model code

from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the car make."
        )
    description = models.TextField(
        blank=True,
        help_text="A brief description of the car make."
        )
    country_of_origin = models.CharField(
        max_length=100,
        blank=True,
        help_text="The country where the car make originates."
    )
    established_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The year the car make was established."
        )

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    # Relationship to CarMake
    car_make = models.ForeignKey(
        'CarMake',
        on_delete=models.CASCADE,
        related_name='car_models',
        help_text="The car make this model belongs to."
    )

    # Fields
    name = models.CharField(
        max_length=100,
        help_text="The name of the car model."
        )

    TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
    ]

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        help_text="The type of car model."
        )
    year = models.IntegerField(
        default=2023,
        help_text="The year this car model was manufactured."
        )
    color = models.CharField(
        max_length=50,
        blank=True, help_text="The color of the car model."
        )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
        # Combines car make and model name
