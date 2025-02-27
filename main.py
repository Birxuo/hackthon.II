from flask import Flask, jsonify, render_template
from flask_cors import CORS
from modules.network_monitor import NetworkMonitor
from modules.predictive_maintenance import PredictiveMaintenance
from modules.cost_optimizer import CostOptimizer
from modules.energy_efficiency import EnergyEfficiency
from modules.procurement_analyzer import ProcurementAnalyzer
from modules.network_designer import NetworkDesigner
from modules.resource_optimizer import ResourceOptimizer

app = Flask(__name__)
CORS(app)

# Initialize modules
network_monitor = NetworkMonitor()
predictive_maintenance = PredictiveMaintenance()
cost_optimizer = CostOptimizer()
energy_efficiency = EnergyEfficiency()
procurement_analyzer = ProcurementAnalyzer()
network_designer = NetworkDesigner()
resource_optimizer = ResourceOptimizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/network/status', methods=['GET'])
def get_network_status():
    return jsonify(network_monitor.get_status())

@app.route('/api/maintenance/predictions', methods=['GET'])
def get_maintenance_predictions():
    return jsonify(predictive_maintenance.get_predictions())

@app.route('/api/cost/analysis', methods=['GET'])
def get_cost_analysis():
    return jsonify(cost_optimizer.get_analysis())

@app.route('/api/energy/metrics', methods=['GET'])
def get_energy_metrics():
    return jsonify(energy_efficiency.get_metrics())

@app.route('/api/procurement/analysis', methods=['GET'])
def get_procurement_analysis():
    return jsonify(procurement_analyzer.get_analysis())

@app.route('/api/network/design', methods=['GET'])
def get_network_design():
    return jsonify(network_designer.get_design_plan())

@app.route('/api/resource/optimization', methods=['GET'])
def get_resource_optimization():
    infrastructure_data = {}
    return jsonify(resource_optimizer.analyze_asset_utilization(infrastructure_data))

if __name__ == '__main__':
    app.run(debug=True, port=5000)