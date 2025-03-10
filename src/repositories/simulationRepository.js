const Simulation = require('../models/simulation');

class SimulationRepository {
    async saveSimulation(data) {
        const simulation = new Simulation(data);
        return await simulation.save();
    }
    async getAllSimulations() {
        return await Simulation.find().sort({ createdAt: -1 });
    }
    async getSimulationById(id) {
        return await Simulation.findById(id);
    }
}

module.exports = new SimulationRepository();