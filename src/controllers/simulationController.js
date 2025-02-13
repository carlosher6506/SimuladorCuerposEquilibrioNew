const Simulation = require('../models/simulation');

// Guardar una simulación
exports.saveSimulation = async (req, res) => {
    try {
        const { weight, theta1, theta2, tension1, tension2 } = req.body;
        const simulation = new Simulation({ weight, theta1, theta2, tension1, tension2 });
        await simulation.save();
        res.status(201).json(simulation);
    } catch (error) {
        res.status(500).json({ message: 'Error guardando la simulación', error });
    }
};

// Obtener todas las simulaciones
exports.getSimulations = async (req, res) => {
    try {
        const simulations = await Simulation.find().sort({ createdAt: -1 });
        res.status(200).json(simulations);
    } catch (error) {
        res.status(500).json({ message: 'Error obteniendo las simulaciones', error });
    }
};

// Obtener una simulación por ID
exports.getSimulationById = async (req, res) => {
    try {
        const simulation = await Simulation.findById(req.params.id);
        if (!simulation) {
            return res.status(404).json({ message: 'Simulación no encontrada' });
        }
        res.status(200).json(simulation);
    } catch (error) {
        res.status(500).json({ message: 'Error obteniendo la simulación', error });
    }
};