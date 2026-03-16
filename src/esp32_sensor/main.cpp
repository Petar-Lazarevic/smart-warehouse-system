/**
 * @file main.cpp
 * @author Petar Lazarevic
 * @brief Edge node logic for RFID data acquisition and MQTT transmission.
 * @version 1.1
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

// Network and MQTT Credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "192.168.100.16"; // Use your Raspberry IP address here
const char* topic = "warehouse/rfid";

// Hardware pins mapping
#define SS_PIN 21
#define RST_PIN 22

MFRC522 rfid(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
    delay(10);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
}

void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        if (client.connect("ESP32_Sensor_Node")) {
            client.publish("warehouse/status", "ESP32 Connected");
        } else {
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    SPI.begin();
    rfid.PCD_Init(); // Initialize RFID reader
    setup_wifi();
    client.setServer(mqtt_server, 1883); // Standard MQTT port
}

void loop() {
    if (!client.connected()) reconnect();
    client.loop();

    // Look for new RFID tags
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
        String cardID = "";
        for (byte i = 0; i < rfid.uid.size; i++) {
            cardID += String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
            cardID += String(rfid.uid.uidByte[i], HEX);
        }
        cardID.toUpperCase();
        
        Serial.println("Tag Detected: " + cardID);
        client.publish(topic, cardID.c_str()); // Send to Broker
        
        rfid.PICC_HaltA(); // Stop reading the same tag
        rfid.PCD_StopCrypto1();
    }
}
