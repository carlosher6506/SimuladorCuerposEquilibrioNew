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