import psutil
import time
import numpy as np
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.history = []
        self.threshold = 0.8  # 80% threshold for alerts

    def collect_metrics(self):
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'timestamp': datetime.now().isoformat()
        }

    def analyze_traffic(self):
        if len(self.history) < 2:
            return None

        current = self.history[-1]
        previous = self.history[-2]
        time_diff = (datetime.fromisoformat(current['timestamp']) - 
                    datetime.fromisoformat(previous['timestamp'])).total_seconds()

        return {
            'bandwidth_usage': (current['bytes_recv'] - previous['bytes_recv']) / time_diff,
            'packet_loss_rate': 1 - (current['packets_recv'] / current['packets_sent']),
            'network_latency': np.random.normal(20, 5)  # Simulated latency in ms
        }

    def get_status(self):
        metrics = self.collect_metrics()
        self.history.append(metrics)
        if len(self.history) > 100:  # Keep last 100 records
            self.history.pop(0)

        analysis = self.analyze_traffic()
        if not analysis:
            return {'status': 'initializing', 'metrics': metrics}

        # Add alerts based on thresholds
        alerts = []
        if analysis['packet_loss_rate'] > self.threshold:
            alerts.append('High packet loss detected')
        if analysis['network_latency'] > 50:  # 50ms threshold
            alerts.append('High network latency detected')

        return {
            'status': 'normal' if not alerts else 'warning',
            'metrics': metrics,
            'analysis': analysis,
            'alerts': alerts
        }