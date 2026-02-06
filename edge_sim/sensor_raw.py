import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # Ini cara import yang benar di v2.0
import time
import random

# Tambahkan parameter CallbackAPIVersion.VERSION2
client = mqtt.Client(CallbackAPIVersion.VERSION2, "Sensor_Sim_01")
client.connect("localhost", 1883)

print("Simulasi Sensor Aktif: Mengirim data vibrasi NORMAL...")

while True:
    # Mengirim data acak di kisaran 0.010 - 0.015 g (Kondisi Sehat)
    # Simulasi LOOSENESS (Data berantakan/high variance)
    # Nilai melonjak-lonjak antara 0.04 dan 0.15
    val = round(random.uniform(0.04, 0.15), 4)
    payload = {"asset": "PUMP_01", "point": "DE", "raw": val}
    
    client.publish("vibration/raw/PUMP_01/DE", str(val)) # Mengirim nilai mentah
    time.sleep(0.5) # Frekuensi 2Hz