from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """Model representing a car manufacturer."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)  # Store NULL if no description

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Model representing a car model with a foreign key to CarMake."""
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-one relationship
    dealer_id = models.IntegerField()
    # Name should not be unique globally but unique within a specific car make
    name = models.CharField(max_length=150)

    # Choices for the 'type' field
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    CAR_TYPE_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon")]

    type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.IntegerField(
        default=2020,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    class Meta:
        unique_together = ('car_make', 'name')  # Ensures uniqueness within each car brand

    def __str__(self):
        return self.name
