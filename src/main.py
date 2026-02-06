import yaml
import time
from engine.ring_buffer import RingBuffer
from engine.l1_processor import L1Processor
from engine.fault_fsm import EarlyFaultFSM
from engine.baseline_mgr import BaselineManager
from diagnostics.l2_diagnostic import L2Diagnostic
from mapping.scada_mapper import ScadaMapper
from drivers.mqtt_manager import MQTTManager
import os
print(f"Mencoba membaca file di: {os.path.abspath('config/safety_params.yaml')}")

# Inisialisasi komponen secara global agar bisa diakses di callback
buffer = RingBuffer(size=50)
processor = L1Processor()
with open('config/safety_params.yaml', 'r') as f:
    safety_cfg = yaml.safe_load(f)

fsm = EarlyFaultFSM(safety_cfg)
baseline = BaselineManager(safety_cfg)
l2_diag = L2Diagnostic()
mapper = ScadaMapper()
tesla_scada = MQTTManager(config_path='config/scada_config.yaml')

def on_message_raw(client, userdata, msg):
    """Fungsi ini dipanggil setiap kali sensor_raw.py mengirim data"""
    try:
        # 1. Terima data mentah
        raw_val = float(msg.payload.decode())
        
        # 2. Masukkan ke Buffer
        buffer.add(raw_val)

        if buffer.is_ready():
            # 3. Ekstraksi Fitur L1
            features = processor.extract(buffer.get_all())
            
            # 4. Cek Deviasi & Update Baseline (Safety: Normal Only)
            is_anomaly = baseline.check_deviation(features, fsm.state)
            
            # 5. Decision Domain (FSM 3-6-10)
            current_state = fsm.process_hit(is_anomaly)

            # 6. Action Domain (Diagnostic)
            diag_report = None
            if current_state in ["WARNING", "ALARM"]:
                diag_report = l2_diag.run(features)

            # 7. Publish ke TeslaSCADA
            spb_metrics, json_meta = mapper.format(current_state, diag_report)
            tesla_scada.publish_spb(spb_metrics)
            if json_meta:
                tesla_scada.publish_json(json_meta)
                
            print(f"[PROCESS] State: {current_state} | Val: {raw_val} | Anomaly: {is_anomaly}")

    except Exception as e:
        print(f"[ERROR] Logic Error: {e}")

# Setup Subscriber untuk data dari Edge Sensor
tesla_scada.client.subscribe("vibration/raw/+/+")
tesla_scada.client.on_message = on_message_raw

print("Vibralyzer Engine is Running. Waiting for sensor data...")
# Jaga agar script tetap hidup
while True:
    time.sleep(1)