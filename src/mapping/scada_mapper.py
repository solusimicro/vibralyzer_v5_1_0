# src/mapping/scada_mapper.py
import time

class ScadaMapper:
    def __init__(self):
        # Mapping prioritas berdasarkan status FSM
        self.priority_map = {
            "NORMAL": "LOW",
            "WATCH": "LOW",
            "WARNING": "MEDIUM",
            "ALARM": "HIGH"
        }

    def format(self, state, diagnostic_report=None):
        """
        Menghasilkan payload SpB (DDATA) dan JSON Metadata.
        """
        timestamp = int(time.time() * 1000)
        
        # --- A. SPARKPLUG B PAYLOAD (Core Metrics) ---
        spb_metrics = [
            {"name": "STATE", "type": "String", "value": state},
            {"name": "CONFIDENCE", "type": "Float", "value": diagnostic_report.get('confidence', 0.0) if diagnostic_report else 1.0},
            {"name": "ACTION_PRIORITY", "type": "String", "value": self.priority_map.get(state, "LOW")}
        ]

        # Invariant: Tambahkan Fault Metrics & Recommendation jika STATE != NORMAL
        json_metadata = None
        if state != "NORMAL" and diagnostic_report:
            # Tambahkan ke SpB DDATA
            spb_metrics.append({"name": "FAULT_CATEGORY", "type": "String", "value": diagnostic_report['category']})
            spb_metrics.append({"name": "RECOMMENDATION", "type": "String", "value": diagnostic_report['recommendation']})

            # --- B. JSON METADATA (Untuk Dashboard Detail di teslaSCADA) ---
            json_metadata = {
                "asset_status": state,
                "diagnostic": diagnostic_report['category'],
                "action": diagnostic_report['recommendation'],
                "evidence": diagnostic_report.get('dominant_feature', 'N/A'),
                "timestamp": timestamp
            }

        return spb_metrics, json_metadata