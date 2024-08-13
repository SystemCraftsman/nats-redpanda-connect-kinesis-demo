import boto3
import json
import random
import time
from datetime import datetime

# Initialize a Kinesis client
kinesis_client = boto3.client('kinesis')

# Define the stream name
stream_name = 'vehicle_data'


# Function to simulate real-time vehicle data
def generate_vehicle_data(vehicle_id):
    data = {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "location": {
            "latitude": round(random.uniform(-90.0, 90.0), 6),
            "longitude": round(random.uniform(-180.0, 180.0), 6)
        },
        "speed": round(random.uniform(0, 120), 2),  # speed in km/h
        "fuel_level": round(random.uniform(0, 100), 2)  # fuel level percentage
    }
    return data


# Function to produce a message to Kinesis
def produce_message(data, partition_key):
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(data),
        PartitionKey=partition_key
    )
    return response


if __name__ == "__main__":
    vehicle_ids = ["vehicle_1", "vehicle_2", "vehicle_3"]  # Example vehicle IDs

    while True:
        for vehicle_id in vehicle_ids:
            vehicle_data = generate_vehicle_data(vehicle_id)
            partition_key = vehicle_id  # Using vehicle ID as the partition key
            response = produce_message(vehicle_data, partition_key)
            print(f"Sent data for {vehicle_id}: {response}")

        time.sleep(1)  # Wait 1 second before sending the next batch of data
