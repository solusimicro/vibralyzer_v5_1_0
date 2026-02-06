# src/engine/baseline_mgr.py snippet

   
class BaselineManager:
    def __init__(self, config):
        self.threshold_multiplier = 2.5 # Contoh: Anomali jika > 2.5x baseline
        self.baseline_value = None
        self.samples_collected = 0
        self.min_samples = config['baseline']['min_samples']

    def check_deviation(self, features, current_state):
        val = features['acc_rms_g']
        
        # Inisialisasi awal
        if self.baseline_value is None:
            self.baseline_value = val
            return False

        # SAFETY INVARIANT: Hanya belajar jika status NORMAL
        if current_state == "NORMAL" and self.samples_collected < self.min_samples:
            self.baseline_value = (0.95 * self.baseline_value) + (0.05 * val)
            self.samples_collected += 1

        # Cek apakah menyimpang dari baseline
        return val > (self.baseline_value * self.threshold_multiplier)
      
    def update_baseline(self, new_value, current_fsm_state):
        # SAFETY INVARIANT: Freeze update jika status bukan NORMAL
        if current_fsm_state == "NORMAL":
            # Gunakan Moving Average atau Exponential Decay
            self.baseline_value = (self.alpha * new_value) + (1 - self.alpha) * self.baseline_value
        else:
            # Lock baseline saat mulai terdeteksi anomali (WATCH/WARNING/ALARM)
            pass
 