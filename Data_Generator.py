import os
import json
import random
from datetime import datetime, timedelta

no_of_files = 5000
out_dir = os.path.join(os.path.dirname(__file__), 'tmp/flights')  # output folder path
cities = [f'City_{i}' for i in range(100, 200)]  # List of city names

probability_of_null_values = random.uniform(0.005, 0.001)  # NULL values


# create random date between a range
def generating_random_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 1, 1)
    total = end_date - start_date
    return start_date + timedelta(days=random.randint(0, total.days))


def randomly_generated_flights_data():

    """Generate a random flight record, with  NULLs in any field"""
    origin_city = random.choice(cities)
    destination_city = random.choice([city for city in cities if city != origin_city])

    record = {
        'date': generating_random_date().isoformat(),
        'origin_city': origin_city,
        'destination_city': destination_city,
        'flight_duration_secs': random.randint(1800, 14400),
        'passengers_on_board': random.randint(50, 300)
    }

    # adding null values randomly
    if random.random() < probability_of_null_values:
        record[random.choice(list(record.keys()))] = None
    return record


# Generate JSON files
def generate_json_files():
    os.makedirs(out_dir, exist_ok=True)
    for _ in range(no_of_files):
        num_records = random.randint(50, 100)
        origin_city = random.choice(cities)
        month_year = datetime.now().strftime("%m-%y")
        filename = f"{out_dir}/{month_year}-{origin_city}-flights.json"

        # Create a list of random flight records
        records = [randomly_generated_flights_data() for _ in range(num_records)]

        with open(filename, 'w') as f:
            json.dump(records, f)

    print(f"Generated {no_of_files} JSON files in {out_dir}")


if __name__ == "__main__":
    generate_json_files()
