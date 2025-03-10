const simulationRepository = require('../repositories/simulationRepository');

class SimulationUseCase {
    async createSimulation(data) {
        return await simulationRepository.saveSimulation(data);
    }
    async listSimulations() {
        return await simulationRepository.getAllSimulations();
    }
    async getSimulation(id) {
        return await simulationRepository.getSimulationById(id);
    }
}
module.exports = new SimulationUseCase();