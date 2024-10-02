# Efficient Data Stream Anomaly Detection

This project simulates a data stream (a sine wave with random anomalies) and uses a Z-Score based anomaly detection algorithm to identify outliers. The data is streamed to a Kafka topic which is consumed by the anomaly detector. The anomalies are then visualized using `matplotlib`.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)

## Project Overview

The goal of this project is to simulate a continuous data stream and detect anomalies in real-time. The data consists of a sine wave with occasional random spikes (anomalies). Kafka is used to simulate a real-time stream of data.

An anomaly detection algorithm based on the Z-Score method is applied to flag values that deviate significantly from the normal pattern. The detected anomalies are visualized using `matplotlib`.

## Features

- Simulates a data stream of sine wave values with random anomalies.
- Sends data to a Kafka topic (`raw-data`).
- Uses Z-Score based anomaly detection.
- Visualizes the data stream and detected anomalies using `matplotlib`.

## Installation

1. Clone this repository:  
   ```bash git clone https://github.com/your-repo/efficient-data-stream-anomaly-detection.git cd efficient-data-stream-anomaly-detection```

2.  Install dependencies:  
```pip install -r requirements.txt```

3. Install and run Kafka and Zookeeper:  
```bin/zookeeper-server-start.sh config/zookeeper.properties```  
```bin/kafka-server-start.sh config/server.properties```

4. Create a Kafka topic (raw-data)  
```bin/kafka-topics.sh --create --topic raw-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1```

## Usage
Run the `kafka-stream.py` script to generate and stream data to Kafka:  
```python kafka-stream.py```


Detect anomalies:  
`python anomaly-detector-kafka.py`
