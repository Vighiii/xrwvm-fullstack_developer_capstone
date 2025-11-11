// app.js
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const Car = require('./models/car');

const app = express();
const PORT = 3000;
const MONGODB_URI = 'mongodb://localhost:27017/carDB';

// Conexión a MongoDB
mongoose.connect(MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Conectado a MongoDB'))
  .catch(err => console.error('Error de conexión a MongoDB:', err));

// Middleware para parsear JSON
app.use(express.json());

// Punto de entrada raíz
app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Cargar datos desde car_records.json y guardarlos en MongoDB
app.post('/load-data', async (req, res) => {
  try {
    const data = fs.readFileSync('car_records.json', 'utf8');
    const cars = JSON.parse(data).cars;

    await Car.insertMany(cars);
    res.status(201).send('Datos cargados correctamente en MongoDB');
  } catch (error) {
    res.status(500).send('Error al cargar los datos: ' + error.message);
  }
});

// i. Endpoint para recuperar autos por ID del concesionario
app.get('/cars/:id', async (req, res) => {
  try {
    const cars = await Car.find({ dealer_id: req.params.id });
    if (cars.length === 0) return res.status(404).send('No se encontraron autos para el concesionario especificado.');
    res.json(cars);
  } catch (error) {
    res.status(500).send('Error al recuperar los datos: ' + error.message);
  }
});

// ii. Endpoint para recuperar autos por ID del concesionario y marca
app.get('/carsbymake/:id/:make', async (req, res) => {
  try {
    const cars = await Car.find({ dealer_id: req.params.id, make: req.params.make });
    if (cars.length === 0) return res.status(404).send('No se encontraron autos para el concesionario y la marca especificados.');
    res.json(cars);
  } catch (error) {
    res.status(500).send('Error al recuperar los datos: ' + error.message);
  }
});

// iii. Endpoint para recuperar autos por ID del concesionario y modelo
app.get('/carsbymodel/:id/:model', async (req, res) => {
  try {
    const cars = await Car.find({ dealer_id: req.params.id, model: req.params.model });
    if (cars.length === 0) return res.status(404).send('No se encontraron autos para el concesionario y el modelo especificados.');
    res.json(cars);
  } catch (error) {
    res.status(500).send('Error al recuperar los datos: ' + error.message);
  }
});

// iv. Endpoint para recuperar autos por ID del concesionario y kilometraje máximo
app.get('/carsbymaxmileage/:id/:mileage', async (req, res) => {
  try {
    const cars = await Car.find({ dealer_id: req.params.id, mileage: { $lte: req.params.mileage } });
    if (cars.length === 0) return res.status(404).send('No se encontraron autos para el concesionario con el kilometraje especificado.');
    res.json(cars);
  } catch (error) {
    res.status(500).send('Error al recuperar los datos: ' + error.message);
  }
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
