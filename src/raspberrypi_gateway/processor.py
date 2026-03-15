"""
@file processor.py
@author Petar Lazarevic
@brief IoT Gateway Service for Warehouse Management.
@details Acts as an intermediary (M2M) that receives MQTT payloads from ESP32 nodes,
         maps RFID UIDs to product names, and persists the data into SQLite.
"""

import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

# Simulated inventory dictionary
# In a production environment, this would be fetched from a master DB table
inventory_map = {
    "6E 9E 08 05": "Yenkee Keyboard",
    "05 81 A1 74 62 43 00": "Samsung 24 Monitor",
    "4B 80 06 81": "Hama Wired Mouse"
}

def init_db():
    """
    Initializes the local SQLite database and creates the logs table if it doesn't exist.
    Demonstrates basic Schema design for IoT logging.
    """
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  rfid_id TEXT, item TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def on_message(client, userdata, message):
    """
    Callback function triggered upon receiving an MQTT message.
    Handles data decoding, inventory lookup, and database persistence.
    """
    # Decode incoming RFID payload
    rfid_id = str(message.payload.decode("utf-8")).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Map the UID to a human-readable item name
    item_name = inventory_map.get(rfid_id, "Unknown Item")

    # Database processing
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    # Using parameterized queries to prevent SQL injection
    c.execute("INSERT INTO logs (rfid_id, item, timestamp) VALUES (?, ?, ?)", 
              (rfid_id, item_name, timestamp))
    conn.commit()
    conn.close()
    print(f"Logged: {item_name} ({rfid_id}) at {timestamp}")

# Execution
init_db()
# Initialize MQTT client using the latest API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_message = on_message
client.connect("192.168.100.16", 1883) # Update this IP with your Raspberry Pi's actual network address
client.subscribe("warehouse/rfid")
client.loop_forever() # Continuous operation
