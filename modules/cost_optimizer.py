import numpy as np
from datetime import datetime, timedelta
import logging

class CostOptimizer:
    """
    Analyzes and optimizes infrastructure costs with improved predictive capabilities
    and more robust recommendations.
    """
    def __init__(self, base_infrastructure_cost=10000, energy_cost_per_kwh=0.12):
        """
        Initialize the CostOptimizer with configurable base costs.
        
        Args:
            base_infrastructure_cost (float): Base monthly infrastructure cost
            energy_cost_per_kwh (float): Cost per kilowatt-hour
        """
        self.base_infrastructure_cost = base_infrastructure_cost
        self.energy_cost_per_kwh = energy_cost_per_kwh
        self.maintenance_cost_history = []
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Set up logging for the CostOptimizer."""
        logger = logging.getLogger("CostOptimizer")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def calculate_energy_costs(self, daily_usage_mean=240, daily_usage_std=20):
        """
        Calculate monthly energy costs based on configurable usage patterns.
        
        Args:
            daily_usage_mean (float): Average daily kWh usage
            daily_usage_std (float): Standard deviation of daily usage
            
        Returns:
            float: Total monthly energy cost
        """
        daily_usage = np.random.normal(daily_usage_mean, daily_usage_std)
        monthly_usage = daily_usage * 30
        cost = monthly_usage * self.energy_cost_per_kwh
        self.logger.debug(f"Calculated energy cost: ${cost:.2f} based on {monthly_usage:.2f} kWh")
        return cost

    def calculate_maintenance_costs(self, include_emergency=True):
        """
        Calculate monthly maintenance costs with option to exclude emergency maintenance.
        
        Args:
            include_emergency (bool): Whether to include emergency maintenance costs
            
        Returns:
            dict: Breakdown of maintenance costs
        """
        routine_maintenance = np.random.normal(500, 50)
        emergency_maintenance = np.random.normal(200, 100) if include_emergency else 0
        
        maintenance_costs = {
            'routine': routine_maintenance,
            'emergency': emergency_maintenance,
            'total': routine_maintenance + emergency_maintenance
        }
        
        self.maintenance_cost_history.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'costs': maintenance_costs
        })
        
        return maintenance_costs

    def calculate_bandwidth_costs(self, base_cost=2000, usage_mean=1.1, usage_std=0.1):
        """
        Calculate bandwidth costs with configurable parameters.
        
        Args:
            base_cost (float): Base bandwidth cost
            usage_mean (float): Mean usage multiplier
            usage_std (float): Standard deviation of usage multiplier
            
        Returns:
            dict: Bandwidth cost breakdown
        """
        usage_multiplier = np.random.normal(usage_mean, usage_std)
        total_cost = base_cost * usage_multiplier
        
        return {
            'base_cost': base_cost,
            'usage_multiplier': usage_multiplier,
            'total_cost': total_cost
        }

    def predict_future_costs(self, months=3, include_confidence_interval=True):
        """
        Predict costs for future months with confidence intervals.
        
        Args:
            months (int): Number of months to predict
            include_confidence_interval (bool): Whether to include confidence intervals
            
        Returns:
            list: Predicted costs for specified months
        """
        future_costs = []
        for month in range(1, months + 1):
            predicted_mean = np.random.normal(15000, 1000)
            
            predicted_cost = {
                'month': (datetime.now() + timedelta(days=30*month)).strftime('%Y-%m'),
                'predicted_total': predicted_mean
            }
            
            if include_confidence_interval:
                predicted_cost['confidence_interval'] = {
                    'lower_bound': predicted_mean * 0.9,
                    'upper_bound': predicted_mean * 1.1
                }
                
            future_costs.append(predicted_cost)
            
        return future_costs

    def get_cost_reduction_recommendations(self, current_costs):
        """
        Generate cost reduction recommendations based on current costs.
        
        Args:
            current_costs (dict): Current cost breakdown
            
        Returns:
            list: Recommended cost reduction actions
        """
        recommendations = []
        
        # Energy cost recommendations
        if current_costs['energy_costs'] > 1000:
            recommendations.append({
                'category': 'Energy',
                'action': 'Implement power management schedules',
                'estimated_savings': '15-20%',
                'implementation_difficulty': 'Medium',
                'priority': 'High'
            })
            recommendations.append({
                'category': 'Energy',
                'action': 'Investigate renewable energy options',
                'estimated_savings': '10-30%',
                'implementation_difficulty': 'High',
                'priority': 'Medium'
            })

        # Maintenance cost recommendations
        if current_costs['maintenance_costs']['total'] > 800:
            recommendations.append({
                'category': 'Maintenance',
                'action': 'Optimize maintenance schedules based on predictive analytics',
                'estimated_savings': '20-25%',
                'implementation_difficulty': 'Medium',
                'priority': 'High'
            })
            
            if current_costs['maintenance_costs'].get('emergency', 0) > 300:
                recommendations.append({
                    'category': 'Maintenance',
                    'action': 'Implement proactive monitoring to reduce emergency maintenance',
                    'estimated_savings': '30-40% of emergency costs',
                    'implementation_difficulty': 'Medium',
                    'priority': 'Critical'
                })

        # Bandwidth cost recommendations
        if current_costs['bandwidth_costs']['total'] > 2200:
            recommendations.append({
                'category': 'Bandwidth',
                'action': 'Implement traffic optimization and caching',
                'estimated_savings': '10-15%',
                'implementation_difficulty': 'Medium',
                'priority': 'High'
            })
            recommendations.append({
                'category': 'Bandwidth',
                'action': 'Negotiate volume discounts with providers',
                'estimated_savings': '5-10%',
                'implementation_difficulty': 'Low',
                'priority': 'Medium'
            })

        return recommendations

    def get_analysis(self):
        """
        Generate comprehensive cost analysis and recommendations.
        
        Returns:
            dict: Complete cost analysis
        """
        maintenance_costs = self.calculate_maintenance_costs()
        bandwidth_costs = self.calculate_bandwidth_costs()
        
        current_costs = {
            'energy_costs': self.calculate_energy_costs(),
            'maintenance_costs': maintenance_costs,
            'bandwidth_costs': bandwidth_costs,
            'infrastructure_costs': self.base_infrastructure_cost
        }

        total_cost = (current_costs['energy_costs'] + 
                     maintenance_costs['total'] + 
                     bandwidth_costs['total'] + 
                     self.base_infrastructure_cost)
        
        historical_trend = None
        if len(self.maintenance_cost_history) > 1:
            # Calculate trend if we have historical data
            oldest = self.maintenance_cost_history[0]['costs']['total']
            newest = self.maintenance_cost_history[-1]['costs']['total']
            historical_trend = (newest - oldest) / oldest * 100  # Percentage change
        
        return {
            'current_costs': current_costs,
            'total_monthly_cost': total_cost,
            'historical_trend': historical_trend,
            'cost_breakdown_percentage': {
                'energy': (current_costs['energy_costs'] / total_cost) * 100,
                'maintenance': (maintenance_costs['total'] / total_cost) * 100,
                'bandwidth': (bandwidth_costs['total'] / total_cost) * 100,
                'infrastructure': (self.base_infrastructure_cost / total_cost) * 100
            },
            'future_cost_predictions': self.predict_future_costs(),
            'cost_reduction_recommendations': self.get_cost_reduction_recommendations(current_costs),
            'estimated_annual_savings': self._calculate_potential_savings(current_costs)
        }
    
    def _calculate_potential_savings(self, current_costs):
        """
        Calculate potential annual savings based on implementing all recommendations.
        
        Args:
            current_costs (dict): Current cost breakdown
            
        Returns:
            float: Estimated annual savings
        """
        # Simplified calculation - in a real implementation, this would be more sophisticated
        monthly_total = (current_costs['energy_costs'] + 
                        current_costs['maintenance_costs']['total'] + 
                        current_costs['bandwidth_costs']['total'] + 
                        self.base_infrastructure_cost)
        
        # Estimate 15% savings from all optimizations
        potential_monthly_savings = monthly_total * 0.15
        annual_savings = potential_monthly_savings * 12
        
        return annual_savings