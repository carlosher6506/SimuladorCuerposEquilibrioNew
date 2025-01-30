const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

let simulaciones = []; // Simulaciones almacenadas en memoria

// Ruta para guardar una simulación
app.post('/api/simulaciones', (req, res) => {
    const { angulo1, angulo2, peso } = req.body;

    if (!angulo1 || !angulo2 || !peso) {
        return res.status(400).json({ mensaje: 'Faltan parámetros' });
    }

    const id = simulaciones.length + 1;
    const simulacion = { id, angulo1, angulo2, peso };
    simulaciones.push(simulacion);

    res.status(201).json({ mensaje: 'Simulación guardada', simulacion });
});

// Ruta para obtener todas las simulaciones
app.get('/api/simulaciones', (req, res) => {
    res.json(simulaciones);
});

// Ruta para obtener una simulación específica
app.get('/api/simulaciones/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const simulacion = simulaciones.find(s => s.id === id);

    if (!simulacion) {
        return res.status(404).json({ mensaje: 'Simulación no encontrada' });
    }

    res.json(simulacion);
});

app.listen(port, () => {
    console.log(`API corriendo en http://localhost:${port}`);
});
