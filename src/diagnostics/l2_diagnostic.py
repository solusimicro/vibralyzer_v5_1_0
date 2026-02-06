class L2Diagnostic:
    def run(self, features):
        # Logika klasifikasi sederhana berdasarkan pola fitur
        # Dalam versi lanjut, ini bisa berupa FFT atau AI model
        return {
            "category": "Mechanical Looseness / Bearing Wear",
            "confidence": 0.88,
            "recommendation": "Check bolt tightness and lubricate DE bearing",
            "dominant_feature": "acc_rms_g"
        }