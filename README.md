# Refactorización de API con Arquitectura Limpia

## Problemas Identificados en el Código Original

El código original presentaba varios problemas:

* Acoplamiento entre capas: Los controladores interactuaban directamente con los modelos de Mongoose, lo que creaba una dependencia fuerte entre la capa de presentación y la capa de datos.
* Responsabilidad Única: Los controladores realizaban múltiples responsabilidades: recepción de peticiones, lógica de negocio y acceso a datos.
* Escalamiento: Añadir nuevas características requeriría modificar múltiples partes del código, teniendo cierto riesgo de introducir errores.

## API original

### simulationController

~~~JavaScript
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

simulation: const mongoose = require('mongoose');

const SimulationSchema = new mongoose.Schema({
    weight: { type: Number, required: true },
    theta1: { type: Number, required: true },
    theta2: { type: Number, required: true },
    tension1: { type: Number, required: true },
    tension2: { type: Number, required: true },
    createdAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Simulation', SimulationSchema);
~~~

### simulationRoutes

~~~JavaScript
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
~~~

### Simulation

~~~JavaScript
const mongoose = require('mongoose');

const SimulationSchema = new mongoose.Schema({
    weight: { type: Number, required: true },
    theta1: { type: Number, required: true },
    theta2: { type: Number, required: true },
    tension1: { type: Number, required: true },
    tension2: { type: Number, required: true },
    createdAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Simulation', SimulationSchema);
~~~

### App

~~~JavaScript
require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Conexión a MongoDB
mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
    .then(() => console.log('Conectado a MongoDB'))
    .catch(err => console.error('Error conectando a MongoDB:', err));

// Rutas
app.use('/api/simulations', require('./routes/simulationRoutes'));

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
~~~

## Mejoras Aplicadas

### Nuevas Implementaciones

Se reorganizó el código siguiendo los principios de Arquitectura Limpia, creando y modificando lo siguiente:

* Controllers: Manejo de peticiones HTTP y respuestas (capa más externa).
* Use Cases: Encapsulación de la lógica de negocio.
* Repositories: Abstracción del acceso a datos.
* Simulator: Definición de la estructura de datos.

### Separación de Responsabilidades

Cada componente ahora tiene una responsabilidad clara:

* Los Controllers solo se encargan de recibir peticiones y enviar respuestas.
* Los Use Cases contienen toda la lógica de negocio relacionada con las simulaciones.
* Los Repositories abstraen y centralizan el acceso a la base de datos.

## API refactorizada

### simulationControler

~~~JavaScript
const simulationUseCase = require('../usecases/simulationUseCase');

exports.saveSimulation = async (req, res) => {
    try {
        const simulation = await simulationUseCase.createSimulation(req.body);
        res.status(201).json(simulation);
    } catch (error) {
        res.status(500).json({ message: 'Error guardando la simulación', error });
    }
};

exports.getSimulations = async (req, res) => {
    try {
        const simulations = await simulationUseCase.listSimulations();
        res.status(200).json(simulations);
    } catch (error) {
        res.status(500).json({ message: 'Error obteniendo las simulaciones', error });
    }
};

exports.getSimulationById = async (req, res) => {
    try {
        const simulation = await simulationUseCase.getSimulation(req.params.id);
        if (!simulation) {
            return res.status(404).json({ message: 'Simulación no encontrada' });
        }
        res.status(200).json(simulation);
    } catch (error) {
        res.status(500).json({ message: 'Error obteniendo la simulación', error });
    }
};
~~~

### simulationRepository

~~~JavaScript
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
~~~

### simulationRoute

~~~JavaScript
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
~~~

### simulationUseCase

~~~JavaScript
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
~~~

## Ventajas de la refactorización

* Mejora la separación de responsabilidades.
* Si se hacen pruebas unitarias o cualquier otro tipo de pruebas, será más fácil.
* Mejora la reutilización de código y escalabilidad.
* Se puede cambiar la base de datos sin tener varios cambios.
