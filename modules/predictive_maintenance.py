import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

class PredictiveMaintenance:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.last_maintenance = datetime.now()
        self.equipment_data = []

    def collect_equipment_data(self):
        # Simulate equipment sensor data
        return {
            'temperature': np.random.normal(45, 5),  # Normal operating temp around 45°C
            'vibration': np.random.normal(0.5, 0.1),  # Normal vibration level
            'power_consumption': np.random.normal(100, 10),  # Power usage in watts
            'uptime_hours': (datetime.now() - self.last_maintenance).total_seconds() / 3600
        }

    def train_model(self):
        # Simulate historical data for training
        X = np.random.rand(1000, 4)  # Features: temp, vibration, power, uptime
        y = (X[:, 0] * 0.3 + X[:, 1] * 0.3 + X[:, 2] * 0.2 + X[:, 3] * 0.2 > 0.6).astype(int)
        self.model.fit(X, y)

    def predict_failure_probability(self, data):
        features = np.array([[data['temperature'],
                            data['vibration'],
                            data['power_consumption'],
                            data['uptime_hours']]])
        return self.model.predict_proba(features)[0][1]

    def get_predictions(self):
        if not self.model.n_features_in_:
            self.train_model()

        current_data = self.collect_equipment_data()
        failure_prob = self.predict_failure_probability(current_data)

        # Calculate estimated time to failure
        if failure_prob > 0.7:
            time_to_failure = "Less than 24 hours"
        elif failure_prob > 0.5:
            time_to_failure = "1-3 days"
        elif failure_prob > 0.3:
            time_to_failure = "3-7 days"
        else:
            time_to_failure = "More than 7 days"

        return {
            'current_status': current_data,
            'failure_probability': failure_prob,
            'estimated_time_to_failure': time_to_failure,
            'recommended_actions': self.get_recommended_actions(failure_prob)
        }

    def get_recommended_actions(self, failure_prob):
        if failure_prob > 0.7:
            return ["Immediate maintenance required",
                    "Schedule emergency inspection",
                    "Prepare backup systems"]
        elif failure_prob > 0.5:
            return ["Schedule maintenance within 48 hours",
                    "Monitor system closely",
                    "Review recent performance logs"]
        elif failure_prob > 0.3:
            return ["Schedule routine maintenance",
                    "Continue regular monitoring"]
        else:
            return ["No immediate action required",
                    "Continue regular maintenance schedule"]
