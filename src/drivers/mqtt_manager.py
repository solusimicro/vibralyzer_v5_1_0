import paho.mqtt.client as mqtt
import json
import time
import yaml

class MQTTManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.cfg = yaml.safe_load(f)
        
        # Tambahkan pengecekan ini untuk mempermudah debug
        if self.cfg is None or 'mqtt' not in self.cfg:
            raise ValueError(f"File konfigurasi {config_path} kosong atau strukturnya salah!")

        # Pastikan menggunakan CallbackAPIVersion.VERSION2 karena kita pakai paho-mqtt 2.x
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, 
            client_id=self.cfg['mqtt']['client_id']
        )
        
        # Setup Callbacks untuk Industrial Reliability
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        
        # 2. Inisialisasi Koneksi
        self.connect()

    def connect(self):
        try:
            self.client.connect(
                self.cfg['mqtt']['broker'], 
                self.cfg['mqtt']['port'], 
                keepalive=60
            )
            self.client.loop_start() # Menjalankan background thread untuk network traffic
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        # Catatan: di v2.0 'rc' biasanya disebut 'reason_code'
        if reason_code == 0:
            print("[INFO] Connected to MQTT Broker (TeslaSCADA)")
            self._publish_birth_certificate()
        else:
            print(f"[ERROR] Connection failed with reason code: {reason_code}")
            print("[INFO] Connected to MQTT Broker (TeslaSCADA)")
            # Kirim NBIRTH (Node Birth) sesuai Sparkplug B saat pertama konek
            self._publish_birth_certificate()
       
    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
            print(f"[WARNING] Disconnected from Broker. Reason: {reason_code}")
            # Paho akan otomatis mencoba reconnect jika menggunakan loop_start()

    def _publish_birth_certificate(self):
        """Kirim sinyal bahwa Vibralyzer Node telah aktif (Sparkplug B)"""
        topic = f"spBv1.0/{self.cfg['spb']['group_id']}/NBIRTH/{self.cfg['spb']['node_id']}"
        payload = {"timestamp": int(time.time()*1000), "metrics": []} 
        self.client.publish(topic, json.dumps(payload), qos=1, retain=True)

    def publish_spb(self, metrics_list):
        topic = (f"spBv1.0/{self.cfg['spb']['group_id']}/DDATA/"
                f"{self.cfg['spb']['node_id']}/{self.cfg['spb']['device_id']}")
        
        # Buat dictionary flat: {"STATE": "ALARM", "CONFIDENCE": 0.88, ...}
        flat_metrics = {m['name']: m['value'] for m in metrics_list}
        flat_metrics["timestamp"] = int(time.time() * 1000)
        flat_metrics["seq"] = self._get_next_seq()

        self.client.publish(topic, json.dumps(flat_metrics), qos=1)

    def _get_next_seq(self):
        if not hasattr(self, '_seq'): self._seq = 0
        self._seq = (self._seq + 1) % 256
        return self._seq    

    def publish_json(self, payload):
        """Mengirim metadata diagnostik tambahan (JSON Standar)"""
        topic = f"vibration/l2/{self.cfg['spb']['device_id']}/diag"
        self.client.publish(topic, json.dumps(payload), qos=0)