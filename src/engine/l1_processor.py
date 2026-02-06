import numpy as np

class L1Processor:
    def extract(self, data_array):
        # Menghitung Root Mean Square (RMS) dari sinyal vibrasi
        rms = np.sqrt(np.mean(data_array**2))
        return {
            "acc_rms_g": round(rms, 4),
            "peak": round(np.max(np.abs(data_array)), 4)
        }