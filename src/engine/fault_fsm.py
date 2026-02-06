# src/engine/fault_fsm.py

class EarlyFaultFSM:
    def __init__(self, config):
        self.state = "NORMAL" # [cite: 150]
        self.hit_counter = 0
        self.config = config['persistence']

    def process_hit(self, is_anomaly):
        """
        Mengatur transisi status berdasarkan persistensi[cite: 86, 164].
        """
        if is_anomaly:
            self.hit_counter += 1
            return self._evaluate_escalation()
        else:
            # Butuh pemulihan stabil untuk kembali ke NORMAL [cite: 165]
            self.hit_counter = 0 
            self.state = "NORMAL"
            return self.state

    def _evaluate_escalation(self):
        # NORMAL -> WATCH (3 hits) [cite: 165, 179]
        if self.state == "NORMAL" and self.hit_counter >= self.config['normal_to_watch']:
            self.state = "WATCH"
        
        # WATCH -> WARNING (6 hits) [cite: 165, 179]
        elif self.state == "WATCH" and self.hit_counter >= self.config['watch_to_warning']:
            self.state = "WARNING"
            
        # WARNING -> ALARM (10 hits) [cite: 165, 179]
        elif self.state == "WARNING" and self.hit_counter >= self.config['warning_to_alarm']:
            self.state = "ALARM"
            
        return self.state