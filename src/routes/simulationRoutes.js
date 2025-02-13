const express = require('express');
const { saveSimulation, getSimulations, getSimulationById } = require('../controllers/simulationController');

const router = express.Router();

// Guardar una simulación
router.post('/', saveSimulation);

// Obtener todas las simulaciones
router.get('/', getSimulations);

// Obtener una simulación por ID
router.get('/:id', getSimulationById);

module.exports = router;