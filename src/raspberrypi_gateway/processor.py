"""
Gateway Processor Module
Acts as a bridge between the ESP32 sensor nodes and the central database/web app.
"""

import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

# Simulated inventory dictionary
inventory_map = {
    "6E 9E 08 05": "Yenkee Keyboard",
    "05 81 A1 74 62 43 00": "Samsung 24 Monitor",
    "4B 80 06 81": "Hama Wired Mouse"
}

def init_db():
    conn = sqlite3.connect('warehouse.db') # Lightweight SQLite
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  rfid_id TEXT, item TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def on_message(client, userdata, message):
    """
    Callback for processing incoming RFID data.
    In a production environment, this would involve database I/O operations.
    """
  
    rfid_id = str(message.payload.decode("utf-8")).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = inventory_map.get(rfid_id, "Unknown Item")
    
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (rfid_id, item, timestamp) VALUES (?, ?, ?)", 
              (rfid_id, item_name, timestamp))
    conn.commit()
    conn.close()
    print(f"Logged: {item_name} ({rfid_id}) at {timestamp}")

init_db()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("192.168.100.16", 1883) # Instead of this IP, use your Raspberry Pi IP address
client.subscribe("warehouse/rfid")
client.loop_forever() # Continuous operation
