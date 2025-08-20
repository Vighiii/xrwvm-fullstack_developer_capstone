from django.db import models
from django.core.validators import RegexValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"


class CarModel(models.Model):
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField(
        help_text="ID of the dealer this model belongs to"
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    year = models.IntegerField(
        default=2023,
        validators=[
            RegexValidator(
                regex=r"^(20[0-2][0-9]|2015)$",
                message="Year must be between 2015 and 2023",
            )
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"
