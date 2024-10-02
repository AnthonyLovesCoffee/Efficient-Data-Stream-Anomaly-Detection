import numpy as np
import json
from confluent_kafka import Consumer, KafkaError
import matplotlib.pyplot as plt
from collections import deque

# config the Kafka consumer
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'anomaly-detector-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['raw-data']) 

# deque to store rolling window of data for Z-Score calculation
window_size = 50
data_window = deque(maxlen=window_size)
time_steps = []  
values = []  
anomalies = [] 

# detect anomalies using Z-Score
def detect_anomaly(value, time_step):
    if len(data_window) == window_size:
        mean = np.mean(data_window)
        std = np.std(data_window)
        z_score = abs(value - mean) / std if std != 0 else 0

        if z_score > 3:  # Using Z-Score threshold of 3 for anomaly detection
            anomalies.append({'time_step': time_step, 'value': value, 'z_score': z_score})

    data_window.append(value)

# plot the data stream with anomalies
def plot_data():
    anomaly_steps = [anomaly['time_step'] for anomaly in anomalies]
    anomaly_values = [anomaly['value'] for anomaly in anomalies]

    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, values, label='Data Stream', color='blue')

    if anomalies:
        plt.scatter(anomaly_steps, anomaly_values, color='red', label='Anomalies', marker='x')

    plt.title('Data Stream with Anomalies')
    plt.xlabel('Time Step')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# messages from the Kafka topic
def consume_data():
    print("Starting to consume data from Kafka...")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # decode the message from Kafka
            message = msg.value().decode('utf-8')
            data = json.loads(message)

            time_step = data['time_step']
            value = data['value']

            # time step and value to lists for plotting
            time_steps.append(time_step)
            values.append(value)

            detect_anomaly(value, time_step)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

consume_data()
plot_data()