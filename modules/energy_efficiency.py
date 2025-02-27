import numpy as np
from datetime import datetime, timedelta
import logging
import json

class EnergyEfficiency:
    """
    Monitors and optimizes energy efficiency for infrastructure systems
    with enhanced analytics and reporting capabilities.
    """
    def __init__(self, peak_power_threshold=1000, cooling_efficiency=0.75):
        """
        Initialize the energy efficiency monitor with configurable thresholds.
        
        Args:
            peak_power_threshold (float): Peak power threshold in watts
            cooling_efficiency (float): Initial cooling system efficiency
        """
        self.peak_power_threshold = peak_power_threshold
        self.energy_history = []
        self.cooling_efficiency = cooling_efficiency
        self.logger = self._setup_logger()
        self.anomaly_threshold = 2.0  # Standard deviations for anomaly detection
    
    def _setup_logger(self):
        """Set up logging for the EnergyEfficiency module."""
        logger = logging.getLogger("EnergyEfficiency")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def collect_power_data(self, simulate=True, real_data=None):
        """
        Collect power consumption data from real sources or simulation.
        
        Args:
            simulate (bool): Whether to simulate data
            real_data (dict): Real power data if simulate is False
            
        Returns:
            dict: Power consumption data
        """
        if not simulate and real_data:
            return real_data
            
        # Enhanced simulation with diurnal patterns
        hour_of_day = datetime.now().hour
        
        # Simulate lower power at night, higher during day
        time_factor = 0.7 + 0.6 * np.sin(np.pi * hour_of_day / 12)
        
        power_data = {
            'total_power': np.random.normal(800 * time_factor, 100),  # Total power in watts
            'cooling_power': np.random.normal(200 * time_factor, 30),  # Cooling system power
            'network_power': np.random.normal(400 * time_factor, 50),  # Network equipment power
            'auxiliary_power': np.random.normal(200 * time_factor, 30),  # Auxiliary systems power
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.debug(f"Collected power data: {json.dumps(power_data, default=str)}")
        return power_data

    def calculate_pue(self, power_data):
        """
        Calculate Power Usage Effectiveness (PUE).
        
        Args:
            power_data (dict): Power consumption data
            
        Returns:
            float: PUE value
        """
        # PUE = Total Facility Power / IT Equipment Power
        it_power = power_data['network_power']
        total_power = power_data['total_power']
        
        if it_power <= 0:
            self.logger.warning("IT power is zero or negative, cannot calculate PUE")
            return None
            
        pue = total_power / it_power
        self.logger.debug(f"Calculated PUE: {pue:.2f}")
        return pue
    
    def calculate_dcie(self, power_data):
        """
        Calculate Data Center Infrastructure Efficiency (DCiE).
        
        Args:
            power_data (dict): Power consumption data
            
        Returns:
            float: DCiE value as a percentage
        """
        pue = self.calculate_pue(power_data)
        if pue:
            dcie = (1 / pue) * 100  # Convert to percentage
            return dcie
        return None

    def detect_anomalies(self, power_data):
        """
        Detect anomalies in power consumption.
        
        Args:
            power_data (dict): Current power data
            
        Returns:
            list: Detected anomalies
        """
        if len(self.energy_history) < 5:
            return []  # Need more history for anomaly detection
            
        anomalies = []
        
        # Calculate mean and std for each metric
        for metric in ['total_power', 'cooling_power', 'network_power', 'auxiliary_power']:
            historical_values = [entry[metric] for entry in self.energy_history[-24:]]
            mean = np.mean(historical_values)
            std = np.std(historical_values)
            
            # Check if current value is an anomaly
            z_score = (power_data[metric] - mean) / std if std > 0 else 0
            if abs(z_score) > self.anomaly_threshold:
                anomalies.append({
                    'metric': metric,
                    'current_value': power_data[metric],
                    'historical_mean': mean,
                    'z_score': z_score,
                    'severity': 'High' if abs(z_score) > 3 else 'Medium'
                })
                
        return anomalies

    def get_efficiency_recommendations(self, power_data, pue):
        """
        Generate efficiency recommendations based on power data and PUE.
        
        Args:
            power_data (dict): Power consumption data
            pue (float): Power Usage Effectiveness
            
        Returns:
            list: Efficiency recommendations
        """
        recommendations = []

        if pue > 1.5:
            recommendations.append({
                'category': 'Cooling',
                'action': 'Optimize cooling system settings',
                'potential_savings': '10-15%',
                'implementation_effort': 'Medium',
                'roi_timeline': '3-6 months'
            })
            
            if power_data['cooling_power'] / power_data['total_power'] > 0.3:
                recommendations.append({
                    'category': 'Cooling',
                    'action': 'Investigate free cooling options or economizers',
                    'potential_savings': '15-25%',
                    'implementation_effort': 'High',
                    'roi_timeline': '6-12 months'
                })

        if power_data['total_power'] > self.peak_power_threshold:
            recommendations.append({
                'category': 'Peak Power',
                'action': 'Implement load balancing to reduce peak power consumption',
                'potential_savings': '5-10%',
                'implementation_effort': 'Medium',
                'roi_timeline': '2-4 months'
            })
            
            recommendations.append({
                'category': 'Peak Power',
                'action': 'Stagger equipment startup to reduce inrush current',
                'potential_savings': '3-5%',
                'implementation_effort': 'Low',
                'roi_timeline': '1-2 months'
            })

        if power_data['auxiliary_power'] / power_data['total_power'] > 0.3:
            recommendations.append({
                'category': 'Auxiliary Systems',
                'action': 'Audit and optimize auxiliary power systems',
                'potential_savings': '8-12%',
                'implementation_effort': 'Medium',
                'roi_timeline': '3-5 months'
            })
            
            recommendations.append({
                'category': 'Auxiliary Systems',
                'action': 'Replace older equipment with energy-efficient models',
                'potential_savings': '10-20%',
                'implementation_effort': 'High',
                'roi_timeline': '12-24 months'
            })

        # Add renewable energy recommendation
        recommendations.append({
            'category': 'Renewable Energy',
            'action': 'Explore solar power options for auxiliary systems',
            'potential_savings': '20-30% of auxiliary power',
            'implementation_effort': 'High',
            'roi_timeline': '24-36 months'
        })

        return recommendations

    def predict_energy_trends(self, days=7):
        """
        Predict energy consumption trends for specified number of days.
        
        Args:
            days (int): Number of days to predict
            
        Returns:
            dict: Energy consumption predictions with confidence intervals
        """
        predictions = []
        base_consumption = 800  # Base power consumption in watts
        
        # Use more sophisticated prediction with weekly patterns
        for day in range(days):
            date = datetime.now() + timedelta(days=day)
            day_of_week = date.weekday()  # 0-6 (Monday-Sunday)
            
            # Weekend factor (lower consumption on weekends)
            weekend_factor = 0.8 if day_of_week >= 5 else 1.0
            
            # Hour of day factor (for first prediction of the day)
            hour_factor = 0.7 + 0.6 * np.sin(np.pi * date.hour / 12)
            
            # Add some randomness and seasonal trends
            random_factor = np.random.normal(0, 0.05)
            seasonal_factor = 1.0 + 0.1 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
            
            # Calculate predicted consumption
            predicted_mean = base_consumption * weekend_factor * hour_factor * seasonal_factor * (1 + random_factor)
            
            # Add confidence interval
            confidence = 0.1 * predicted_mean  # 10% confidence interval
            
            prediction = {
                'date': date.strftime('%Y-%m-%d'),
                'predicted_consumption': predicted_mean,
                'confidence_interval': {
                    'lower': predicted_mean - confidence,
                    'upper': predicted_mean + confidence
                },
                'day_type': 'Weekend' if day_of_week >= 5 else 'Weekday'
            }
            predictions.append(prediction)
        
        return {
            'daily_predictions': predictions,
            'weekly_average': np.mean([p['predicted_consumption'] for p in predictions]),
            'trend': 'Increasing' if predictions[-1]['predicted_consumption'] > predictions[0]['predicted_consumption'] else 'Decreasing'
        }

    def get_metrics(self):
        """
        Generate comprehensive energy efficiency metrics and recommendations.
        
        Returns:
            dict: Energy efficiency metrics and recommendations
        """
        power_data = self.collect_power_data()
        self.energy_history.append(power_data)
        
        # Keep last 24 hours of data
        if len(self.energy_history) > 24:
            self.energy_history.pop(0)

        pue = self.calculate_pue(power_data)
        dcie = self.calculate_dcie(power_data)
        anomalies = self.detect_anomalies(power_data)
        
        # Calculate trends if we have enough history
        pue_trend = None
        if len(self.energy_history) > 1:
            previous_pue = self.calculate_pue(self.energy_history[-2])
            if previous_pue and pue:
                pue_trend = ((pue - previous_pue) / previous_pue) * 100  # Percentage change
        
        return {
            'current_power_data': power_data,
            'power_usage_effectiveness': pue,
            'data_center_infrastructure_efficiency': dcie,
            'pue_trend': pue_trend,
            'detected_anomalies': anomalies,
            'efficiency_metrics': {
                'cooling_efficiency': self.cooling_efficiency,
                'power_distribution_efficiency': 0.9 + np.random.normal(0, 0.02),
                'total_system_efficiency': 0.85 + np.random.normal(0, 0.03),
                'renewable_energy_percentage': np.random.normal(5, 1)  # Percentage of power from renewable sources
            },
            'energy_predictions': self.predict_energy_trends(),
            'recommendations': self.get_efficiency_recommendations(power_data, pue),
            'estimated_annual_savings': self._calculate_potential_savings(power_data, pue)
        }
        
    def _calculate_potential_savings(self, power_data, pue):
        """
        Calculate potential annual savings from implementing all recommendations.
        
        Args:
            power_data (dict): Current power data
            pue (float): Current PUE
            
        Returns:
            dict: Estimated savings breakdown
        """
        # Calculate baseline annual energy cost
        daily_energy_kwh = power_data['total_power'] * 24 / 1000  # Convert watts to kWh
        annual_energy_kwh = daily_energy_kwh * 365
        energy_cost_per_kwh = 0.12  # Assumed cost per kWh
        baseline_annual_cost = annual_energy_kwh * energy_cost_per_kwh
        
        # Estimate savings
        cooling_savings = 0
        peak_power_savings = 0
        auxiliary_savings = 0
        
        if pue > 1.5:
            cooling_savings = baseline_annual_cost * 0.15  # 15% savings from cooling optimization
            
        if power_data['total_power'] > self.peak_power_threshold:
            peak_power_savings = baseline_annual_cost * 0.08  # 8% from peak power management
            
        if power_data['auxiliary_power'] / power_data['total_power'] > 0.3:
            auxiliary_savings = baseline_annual_cost * 0.10  # 10% from auxiliary optimization
            
        # Total potential savings
        total_savings = cooling_savings + peak_power_savings + auxiliary_savings
        
        return {
            'baseline_annual_cost': baseline_annual_cost,
            'savings_breakdown': {
                'cooling_optimization': cooling_savings,
                'peak_power_management': peak_power_savings,
                'auxiliary_system_optimization': auxiliary_savings
            },
            'total_potential_savings': total_savings,
            'savings_percentage': (total_savings / baseline_annual_cost) * 100 if baseline_annual_cost > 0 else 0
        }