from .models import CarMake, CarModel

def initiate_car_makes():
    # Create a list of Car maker (CarMake)
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]
    # Create Car Maker Intances
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(
            name=data['name'],
            description=data['description']
        ))

def initiate_car_models():
    # Get the CarMake instances
    nissan = CarMake.objects.get(name="NISSAN")
    mercedes = CarMake.objects.get(name="Mercedes")
    audi = CarMake.objects.get(name="Audi")
    kia = CarMake.objects.get(name="Kia")
    toyota = CarMake.objects.get(name="Toyota")

    # Create CarModel instances with the corresponding Car Maker instances
    car_model_data = [
        {"name":"Pathfinder", "type":"SUV", "year": 2023, "car_make":nissan, "dealer_id":1},
        {"name":"Qashqai", "type":"SUV", "year": 2023, "car_make":nissan, "dealer_id":2},
        {"name":"XTRAIL", "type":"SUV", "year": 2023, "car_make":nissan, "dealer_id":3},
        {"name":"A-Class", "type":"SUV", "year": 2023, "car_make":mercedes, "dealer_id":4},
        {"name":"C-Class", "type":"SUV", "year": 2023, "car_make":mercedes, "dealer_id":5},
        {"name":"E-Class", "type":"SUV", "year": 2023, "car_make":mercedes, "dealer_id":6},
        {"name":"A4", "type":"SUV", "year": 2023, "car_make":audi, "dealer_id":7},
        {"name":"A5", "type":"SUV", "year": 2023, "car_make":audi, "dealer_id":8},
        {"name":"A6", "type":"SUV", "year": 2023, "car_make":audi, "dealer_id":9},
        {"name":"Sorrento", "type":"SUV", "year": 2023, "car_make":kia, "dealer_id":10},
        {"name":"Carnival", "type":"SUV", "year": 2023, "car_make":kia, "dealer_id":11},
        {"name":"Cerato", "type":"Sedan", "year": 2023, "car_make":kia, "dealer_id":12},
        {"name":"Corolla", "type":"Sedan", "year": 2023, "car_make":toyota, "dealer_id":13},
        {"name":"Camry", "type":"Sedan", "year": 2023, "car_make":toyota, "dealer_id":14},
        {"name":"Kluger", "type":"SUV", "year": 2023, "car_make":toyota, "dealer_id":15},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            type=data["type"],
            year=data["year"],
            car_make=data["car_make"],
            dealer_id=data["dealer_id"],
        )

def initiate():
    initiate_car_makes()
    initiate_car_models()
