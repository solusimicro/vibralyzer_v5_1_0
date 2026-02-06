import numpy as np

class L2Diagnostic:
    def __init__(self, config):
        self.cfg = config
        self.min_confidence = config['diagnostics']['min_confidence']

    def perform_analysis(self, data_buffer):
        """
        Menganalisis buffer data untuk menentukan kategori kegagalan.
        """
        values = np.array(data_buffer)
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        # Hitung koefisien variasi untuk melihat stabilitas sinyal
        variation = std_val / mean_val if mean_val > 0 else 0

        # Logika Klasifikasi Sederhana
        if variation > 0.15: # Sinyal sangat tidak stabil
            category = "Mechanical Looseness / Bearing Wear"
            rec = "Check bolt tightness and lubricate DE bearing"
            confidence = 0.85
        elif mean_val > 0.08: # Sinyal tinggi tapi stabil
            category = "Unbalance / Structural Resonance"
            rec = "Check rotor balance and foundation integrity"
            confidence = 0.90
        else:
            category = "General Wear / Misalignment"
            rec = "Schedule routine alignment check"
            confidence = 0.75

        return {
            "category": category,
            "recommendation": rec,
            "confidence": round(confidence, 2)
        }
        
        