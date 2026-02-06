import paho.mqtt.client as mqtt
import time
import random

# Tambahkan parameter CallbackAPIVersion.VERSION2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Sensor_Sim_01")
client.connect("localhost", 1883)

print("Simulasi Sensor Aktif: Mengirim data vibrasi NORMAL...")

while True:
    # Mengirim data acak di kisaran 0.010 - 0.015 g (Kondisi Sehat)
    val = round(random.uniform(0.080, 0.095), 4)
    payload = {"asset": "PUMP_01", "point": "DE", "raw": val}
    
    client.publish("vibration/raw/PUMP_01/DE", str(val)) # Mengirim nilai mentah
    time.sleep(0.5) # Frekuensi 2Hz