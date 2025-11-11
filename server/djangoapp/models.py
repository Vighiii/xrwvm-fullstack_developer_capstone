# Uncomment the following imports before adding the Model code
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
# Ensure 2 blank lines before class definition
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ])
    # Other fields as needed
    
    def __str__(self):
        return self.name  # Return the name as the string representation

class Dealership(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

class Review(models.Model):
    id = models.AutoField(primary_key=True)  # Assuming the id is the primary key
    name = models.CharField(max_length=255)
    dealership = models.IntegerField()  # Reference to the dealership id
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.IntegerField()

    def __str__(self):
        return self.name 







        
