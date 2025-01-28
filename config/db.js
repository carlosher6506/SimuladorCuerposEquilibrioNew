const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Conexión a MongoDB
mongoose.connect('mongodb://localhost:27017/simulaciones', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'Error de conexión a MongoDB:'));
db.once('open', () => {
    console.log('Conectado a la base de datos MongoDB');
});

// Modelo de simulación
const SimulacionSchema = new mongoose.Schema({
    angulo1: { type: Number, required: true },
    angulo2: { type: Number, required: true },
    peso: { type: Number, required: true },
});

const Simulacion = mongoose.model('Simulacion', SimulacionSchema);

// Rutas
app.get('/', (req, res) => {
    res.send('API de simulaciones funcionando');
});

// Crear una nueva simulación
app.post('/api/simulaciones', async (req, res) => {
    try {
        const { angulo1, angulo2, peso } = req.body;
        const nuevaSimulacion = new Simulacion({ angulo1, angulo2, peso });
        await nuevaSimulacion.save();
        res.status(201).json({ mensaje: 'Simulación guardada', simulacion: nuevaSimulacion });
    } catch (error) {
        res.status(500).json({ mensaje: 'Error al guardar la simulación', error });
    }
});

// Obtener todas las simulaciones
app.get('/api/simulaciones', async (req, res) => {
    try {
        const simulaciones = await Simulacion.find();
        res.json(simulaciones);
    } catch (error) {
        res.status(500).json({ mensaje: 'Error al obtener las simulaciones', error });
    }
});

// Obtener una simulación por ID
app.get('/api/simulaciones/:id', async (req, res) => {
    try {
        const simulacion = await Simulacion.findById(req.params.id);
        if (!simulacion) {
            return res.status(404).json({ mensaje: 'Simulación no encontrada' });
        }
        res.json(simulacion);
    } catch (error) {
        res.status(500).json({ mensaje: 'Error al obtener la simulación', error });
    }
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`API corriendo en http://localhost:${port}`);
});
