# Smart Warehouse M2M System

A modular Machine-to-Machine (M2M) system designed for automated inventory tracking. This project demonstrates a full-stack IoT implementation, from hardware data acquisition to a real-time web dashboard.

## 🏗 System Architecture

The system consists of three main components:
1.  **Edge Node (ESP32)**: Captures RFID tag data and publishes it to the network via MQTT.
2.  **M2M Gateway (Raspberry Pi)**: Runs a Mosquitto MQTT broker and a Python processor that maps raw UIDs to product names and logs them into an SQLite database.
3.  **Web Dashboard (Flask)**: Provides a user-friendly interface to monitor inventory logs and real-time statistics.

## 🛠 Tech Stack & Dependencies

### Infrastructure
* **MQTT Broker**: [Mosquitto](https://mosquitto.org/) (Must be installed and running on the Raspberry Pi)
* **Database**: SQLite3 (Lightweight, file-based)

### Software Libraries
* **C++ (PlatformIO)**: `MFRC522`, `PubSubClient`
* **Python**: `Flask`, `paho-mqtt`

## 🚀 Setup & Installation

### 1. Gateway Infrastructure (Raspberry Pi)
First, install and enable the Mosquitto broker:
```bash
sudo apt update && sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
**Note:** Ensure your mosquitto.conf allows external connections by adding listener 1883 and allow_anonymous true.

### 2. Edge Node (ESP32)
#### 1. Open the project in PlatformIO.
#### 2. Navigate to src/esp32_sensor/main.cpp.
#### 3. Update ssid, password, and mqtt_server (your Raspberry Pi IP).
#### 4. Upload the firmware to your ESP32.

### 3. Backend & Web App
#### 1. Install Python dependencies and start the services:

```bash
# Install requirements
pip install -r requirements.txt
# Start the Gateway Processor (handles data logging)
python src/raspberrypi_gateway/processor.py
# Start the Web Dashboard
python src/web_app/app.py
```
#### 2. Access the Dashboard:
Once the Web App is running, open your browser and navigate to:
> `http://localhost:5000` or `http://<your-raspberry-pi-ip>:5000`

**Note for Raspberry Pi users:** If you encounter a "managed environment" error when running `pip`, it is recommended to use a Virtual Environment (`venv`) or install system-wide packages using:
> `sudo apt install python3-paho-mqtt python3-flask`

## 📁 Repository Structure
```text
smart-warehouse-system/
├── src/
│   ├── esp32_sensor/           # ESP32 Firmware (C++)
│   ├── raspberrypi_gateway/    # MQTT Logic & Database Logging (Python)
│   └── web_app/                # Flask Web Dashboard & Templates
├── platformio.ini              # Build configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```
*Developed by Petar Lazarevic*
