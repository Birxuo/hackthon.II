export interface NetworkMetrics {
    nodeId: string;
    timestamp: Date;
    bandwidth: number;
    latency: number;
    powerConsumption: number;
    energyEfficiency?: EnergyEfficiencyMetrics;
}

export interface MaintenancePrediction {
    needsMaintenance: boolean;
    nextMaintenanceDate: Date;
    risk: number;
}

export interface CostOptimization {
    currentCost: number;
    projectedSavings: number;
    recommendations: string[];
}

export interface EnergyEfficiencyMetrics {
    totalPowerConsumption: number;
    efficiencyRating: number;
    carbonFootprint: number;
    recommendations: string[];
}
