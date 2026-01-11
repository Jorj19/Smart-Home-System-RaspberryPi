# Smart Home System – Raspberry Pi Hardware Module

This repository contains the **hardware-side implementation** of my Smart Home System project.

The system runs on a **Raspberry Pi** and exposes a **local REST API (Flask server)** that provides real-time environmental data collected from multiple sensors.  
These values are consumed by a separate **monitoring application** (mobile / web).

---

## Project Overview

The Raspberry Pi acts as a **local data acquisition and processing unit**, responsible for:
- reading sensor data from multiple environmental sensors
- estimating air quality metrics
- simulating additional parameters for alert testing
- exposing the data via a local HTTP server

The monitoring application connects to this server to retrieve sensor values over the local network.

---

## Hardware Components

- **Raspberry Pi 4 model B**
- **DHT22** – temperature & humidity
- **BH1750** – light intensity (lux)
- **MQ-135** – air quality / CO₂ estimation
- **MQ-5** – gas (LPG, methane)
- **MQ-7** – carbon monoxide (CO)
- **MCP3008** – ADC for MQ sensors
  
---
## Hardware Setup

<img width="auto" height="600" alt="image" src="https://github.com/user-attachments/assets/c94b1f84-e062-4232-99fd-8c92f138953c" />

<img width="auto" height="600" alt="image" src="https://github.com/user-attachments/assets/6cf28b06-0c6a-431b-a136-42ed1e972cc8" />


<img width="auto" height="600" alt="image" src="https://github.com/user-attachments/assets/08adfb8f-638c-4259-9051-0cdf9bd8b307" />


##  Provided Sensor Data

The `/sensors` endpoint returns a JSON object containing:

-  **Temperature** (°C)
-  **Humidity** (%)
-  **Light intensity** (lux)
-  **CO₂ (estimated)** (ppm)
-  **TVOC (estimated)** (ppb)
-  **PM2.5 (simulated)** (µg/m³)
-  **Sound level (simulated)** (dB)
-  **Smoke detection** (bool)
-  **CO (estimated)** (ppm)
-  **Air Quality Index**

> Some values (CO₂, TVOC, CO) are **estimated**, and others (PM2.5, sound, smoke) are **simulated**.  
> They are intended for **application logic testing and alert systems**.

---

##  API Endpoint

### `GET /sensors`

Example response:
```json
{
  "air_quality_index": {
    "unitate": "indice",
    "valoare": 25.8
  },
  "co": {
    "unitate": "ppm",
    "valoare": 55.6
  },
  "fum": {
    "unitate": "bool",
    "valoare": 0
  },
  "humidity": {
    "unitate": "%",
    "valoare": 54.2
  },
  "lux": {
    "unitate": "lux",
    "valoare": 67.5
  },
  "mq135_co2": {
    "unitate": "ppm",
    "valoare": 415.9
  },
  "mq5": {
    "unitate": "%",
    "valoare": 6.1
  },
  "mq7": {
    "unitate": "%",
    "valoare": 61.9
  },
  "pm2_5": {
    "unitate": "ug/m3",
    "valoare": 74
  },
  "sunet": {
    "unitate": "dB",
    "valoare": 33
  },
  "temperature": {
    "unitate": "°C",
    "valoare": 26
  },
  "tvoc": {
    "unitate": "ppb",
    "valoare": 445
  }
}

