import csv

PET_FILE = 'pets.csv'

def fetch_pets():
    """Fetch all pets from the file"""
    try:
        with open(PET_FILE, 'r') as file:
            reader = csv.reader(file)
            pets = list(reader)
            return [pet for pet in pets if len(pet) == 7]  # Ensure only valid pets with 7 fields are returned
    except Exception as e:
        raise Exception(f"Error fetching pets: {e}")

def add_pet(pet_id, name, species, age, gender, weight, description):
    """Add a new pet to the file"""
    pet_data = [pet_id, name, species, age, gender, weight, description]

    if len(pet_data) != 7:
        raise Exception("Invalid pet data")

    # Check if pet_id already exists
    pets = fetch_pets()
    for pet in pets:
        if pet[0] == pet_id:
            raise Exception(f"Pet ID {pet_id} already exists!")

    try:
        with open(PET_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(pet_data)
    except Exception as e:
        raise Exception(f"Error adding pet: {e}")

def remove_pet(pet_id):
    """Remove a pet by its ID"""
    pets = fetch_pets()
    updated_pets = [pet for pet in pets if pet[0] != pet_id]

    if len(updated_pets) == len(pets):
        raise Exception(f"Pet ID {pet_id} not found.")

    try:
        with open(PET_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_pets)
    except Exception as e:
        raise Exception(f"Error removing pet: {e}")

def update_pet(pet_id, name=None, species=None, age=None, gender=None, weight=None, description=None):
    """Update an existing pet's information by pet ID"""
    pets = fetch_pets()
    updated_pets = []
    updated = False

    for pet in pets:
        if pet[0] == pet_id:
            updated_pet = list(pet)
            if name:
                updated_pet[1] = name
            if species:
                updated_pet[2] = species
            if age:
                updated_pet[3] = age
            if gender:
                updated_pet[4] = gender
            if weight:
                updated_pet[5] = weight
            if description:
                updated_pet[6] = description
            updated_pets.append(updated_pet)
            updated = True
        else:
            updated_pets.append(pet)

    if updated:
        try:
            with open(PET_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_pets)
        except Exception as e:
            raise Exception(f"Error updating pet: {e}")
    else:
        raise Exception("Pet ID not found.")

def export_pets_to_csv(file_path):
    """Export all pets to a CSV file."""
    try:
        pets = fetch_pets()
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(pets)
    except Exception as e:
        raise Exception(f"Error exporting pets to CSV: {e}")

def import_pets_from_csv(file_path):
    """Import pets from a CSV file."""
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            pets = list(reader)

        # Check if all pets have the correct number of fields (7 fields for each pet)
        if not all(len(pet) == 7 for pet in pets):
            raise ValueError("Invalid data format in CSV file.")

        # Return the imported pets data instead of saving it directly
        return pets

    except Exception as e:
        raise Exception(f"Error importing pets from CSV: {e}")

