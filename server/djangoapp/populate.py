from .models import CarMake, CarModel 

def initiate():
    # Sample data for CarMake
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology", "country": "Japan", "founding_year": 1933},
        {"name": "Mercedes", "description": "Great cars. German technology", "country": "Germany", "founding_year": 1926},
        {"name": "Audi", "description": "Great cars. German technology", "country": "Germany", "founding_year": 1909},
        {"name": "Kia", "description": "Great cars. Korean technology", "country": "South Korea", "founding_year": 1944},
        {"name": "Toyota", "description": "Great cars. Japanese technology", "country": "Japan", "founding_year": 1937},
    ]

    # Create CarMake instances
    car_make_instances = []
    for data in car_make_data:
        car_make_instance = CarMake.objects.create(
            name=data['name'],
            description=data['description'],
            country=data['country'],
            founding_year=data['founding_year'],
        )
        car_make_instances.append(car_make_instance)

    # Sample dealer IDs (replace these with actual dealer IDs as needed)
    sample_dealer_ids = [1, 2, 3, 4, 5]

    # Sample data for CarModel
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": sample_dealer_ids[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": sample_dealer_ids[0]},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": sample_dealer_ids[0]},
        {"name": "A-Class", "type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": sample_dealer_ids[1]},
        {"name": "C-Class", "type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": sample_dealer_ids[1]},
        {"name": "E-Class", "type": "Sedan", "year": 2023, "car_make": car_make_instances[1], "dealer_id": sample_dealer_ids[1]},
        {"name": "A4", "type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": sample_dealer_ids[2]},
        {"name": "A5", "type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": sample_dealer_ids[2]},
        {"name": "A6", "type": "Sedan", "year": 2023, "car_make": car_make_instances[2], "dealer_id": sample_dealer_ids[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": sample_dealer_ids[3]},
        {"name": "Carnival", "type": "Wagon", "year": 2023, "car_make": car_make_instances[3], "dealer_id": sample_dealer_ids[3]},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3], "dealer_id": sample_dealer_ids[3]},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": sample_dealer_ids[4]},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": sample_dealer_ids[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": car_make_instances[4], "dealer_id": sample_dealer_ids[4]},
    ]

    # Create CarModel instances
    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id'] 
        )

    print('Database populated successfully!')

# Call the function to populate the database
if __name__ == "__main__":
    initiate()
