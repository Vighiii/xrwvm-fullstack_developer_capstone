from .models import CarMake, CarModel


def initiate():
    car_data = [
        {
            "make": "Toyota",
            "description": "Toyota vehicles",
            "models": [
                ("Camry", "Sedan", 2022),
                ("Corolla", "Sedan", 2021),
                ("RAV4", "SUV", 2023),
            ],
        },
        {
            "make": "Honda",
            "description": "Honda vehicles",
            "models": [
                ("Civic", "Sedan", 2022),
                ("Accord", "Sedan", 2021),
                ("CR-V", "SUV", 2023),
            ],
        },
        {
            "make": "Ford",
            "description": "Ford vehicles",
            "models": [
                ("Mustang", "Coupe", 2022),
                ("Explorer", "SUV", 2023),
                ("Escape", "SUV", 2021),
            ],
        },
    ]

    for car in car_data:
        make, created = CarMake.objects.get_or_create(
            name=car["make"],
            defaults={"description": car["description"]}
        )

        for model_name, model_type, year in car["models"]:
            CarModel.objects.get_or_create(
                car_make=make,
                name=model_name,
                type=model_type,
                year=year
            )
