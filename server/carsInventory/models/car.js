// models/car.js
const mongoose = require('mongoose');

const carSchema = new mongoose.Schema({
  make: String,
  model: String,
  bodyType: String,
  year: Number,
  dealer_id: Number,
  mileage: Number,
  price: Number
});

module.exports = mongoose.model('Car', carSchema);
