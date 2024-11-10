import os
import json
import time
import numpy as np
from collections import defaultdict, Counter

# input directory 'flights'
inp_dir = os.path.join(os.path.dirname(__file__), 'tmp/flights')


def data_processing():
    """data processing"""
    start_time = time.time()
    total_records = 0
    dirty_records = 0
    flight_durations = defaultdict(list)
    passengers_count = Counter()

    # Load and process files from the directory
    for file_name in os.listdir(inp_dir):
        file_path = os.path.join(inp_dir, file_name)
        with open(file_path) as f:
            data = json.load(f)
            total_records += len(data)

            # Processing each flight record
            for record in data:
                # Skipping None values
                if any(value is None for value in record.values()):
                    dirty_records += 1
                    continue

                # calculate flight duration data
                flight_durations[record['destination_city']].append(record['flight_duration_secs'])

                # Track passenger counts
                passengers_count[record['origin_city']] -= record['passengers_on_board']
                passengers_count[record['destination_city']] += record['passengers_on_board']

    # Calculate statistics for Top 25 destination cities
    avg_durations = {}
    p95_durations = {}
    for city, durations in sorted(flight_durations.items(), key=lambda x: len(x[1]), reverse=True)[:25]:
        avg_durations[city] = np.mean(durations)
        p95_durations[city] = np.percentile(durations, 95)

    # Find cities with max passengers arrived and departed
    most_passengers_arrived = passengers_count.most_common(1)
    most_passengers_left = passengers_count.most_common()[-1]

    # final Calculation
    run_duration = time.time() - start_time
    print("=== Detailed Data Analysis Report ===")
    print(f"Total records processed: {total_records}")
    print(f"Total dirty records: {dirty_records}")
    print(f"Run duration (seconds): {run_duration:.2f}")
    print("\nTop 25 Destination Cities - Avg and P95 Flight Durations:")
    for city in avg_durations:
        print(f"{city}: AVG = {avg_durations[city]:.2f}, P95 = {p95_durations[city]:.2f}")
    print(f"\nCity with max passengers arrived: {most_passengers_arrived[0]}")
    print(f"City with max passengers left: {most_passengers_left[0]}")


if __name__ == "__main__":
    data_processing()
