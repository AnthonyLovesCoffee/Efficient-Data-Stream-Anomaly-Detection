import numpy as np
import json
from confluent_kafka import Producer
import time

# Configure the Kafka producer to connect to localhost:9092
conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)

with open('output.json', 'w') as json_file:

    # function to simulate the data stream
    def simulate_data_stream():
        for time_step in range(1000):
            sine_value = np.sin(2 * np.pi * time_step / 100)  # sine wave pattern
            anomaly = np.random.rand() < 0.01  # 1% chance of anomaly

            if anomaly:
                sine_value += np.random.normal(10, 5)  # adding random spike as our anomoly

            # dictionary to hold the time-step and sine value
            data = {
                'time_step': time_step,
                'value': sine_value
            }

            # convert dictionary to JSON and encode it to bytes
            json_data = json.dumps(data).encode('utf-8')

            # send the encoded JSON to the 'raw-data' Kafka topic
            producer.produce('raw-data', value=json_data)

            # weite the data to the JSON file
            json.dump(data, json_file)
            json_file.write('\n')  

            time.sleep(0.01)

        producer.flush()

    simulate_data_stream()