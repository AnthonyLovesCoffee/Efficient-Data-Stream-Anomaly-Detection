import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON data from the file
def load_data(file_path):
    data = []
    with open(file_path, 'r') as json_file:
        for line in json_file:
            data_point = json.loads(line)
            data.append(data_point)
    return data

# Anomaly detection function using Z-Score
def detect_anomalies(data, window_size=50, threshold=3):
    values = [point['value'] for point in data]
    anomalies = []

    # Compute rolling mean and standard deviation
    for i in range(window_size, len(values)):
        window = values[i-window_size:i]
        mean = np.mean(window)
        std = np.std(window)

        # Z-Score calculation
        if abs(values[i] - mean) > threshold * std:
            anomalies.append({
                'time_step': data[i]['time_step'],
                'value': values[i],
                'z_score': abs(values[i] - mean) / std
            })

    return anomalies

# Plot the data stream with anomalies highlighted
def plot_data_with_anomalies(data, anomalies):
    time_steps = [point['time_step'] for point in data]
    values = [point['value'] for point in data]

    # Extract anomaly points
    anomaly_steps = [anomaly['time_step'] for anomaly in anomalies]
    anomaly_values = [anomaly['value'] for anomaly in anomalies]

    plt.figure(figsize=(10, 6))
    
    # Plot the sine wave data
    plt.plot(time_steps, values, label='Data Stream', color='blue')

    # Highlight the anomalies
    if anomalies:
        plt.scatter(anomaly_steps, anomaly_values, color='red', label='Anomalies', marker='x')

    # Add labels and legend
    plt.title('Data Stream with Anomalies')
    plt.xlabel('Time Step')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# Display the anomalies
def print_anomalies(anomalies):
    if anomalies:
        print(f"Detected {len(anomalies)} anomalies:")
        for anomaly in anomalies:
            print(f"Time Step: {anomaly['time_step']}, Value: {anomaly['value']}, Z-Score: {anomaly['z_score']:.2f}")
    else:
        print("No anomalies detected.")

# Main function to run the anomaly detector and visualization
def run_anomaly_detector(file_path):
    data = load_data(file_path)
    anomalies = detect_anomalies(data, window_size=50, threshold=3)
    
    print_anomalies(anomalies)
    plot_data_with_anomalies(data, anomalies)

# Run the anomaly detector on the generated JSON data
run_anomaly_detector('output.json')