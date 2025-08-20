// server/database/app.js

const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

// Load JSON files (make sure you’re running from the same folder)
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Connect to MongoDB (dbName: dealershipsDB)
mongoose.connect(
  "mongodb://mongo_db:27017/",
  { dbName: 'dealershipsDB', useNewUrlParser: true, useUnifiedTopology: true }
);

// Import the Mongoose models
const Reviews = require('./review');
const Dealerships = require('./dealership');

//
// Seed or overwrite existing collections on startup
//
try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.error("Error seeding data:", error);
}

// === 1) Home route ===
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// === 2) Fetch all reviews ===
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// === 3) Fetch reviews for a particular dealer ===
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

//
// === 4) Fetch all dealerships ===
//
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

//
// === 5) Fetch dealerships in a particular state ===
//
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const stateParam = req.params.state;
    const dealers = await Dealerships.find({ state: stateParam });
    res.json(dealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

//
// === 6) Fetch a single dealer by ID ===
//
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = req.params.id;
    const dealer = await Dealerships.findOne({ id: dealerId });
    if (dealer) {
      res.json(dealer);
    } else {
      res.status(404).json({ message: 'Dealer not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

//
// === 7) Insert a new review ===
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  try {
    const lastReview = await Reviews.find().sort({ id: -1 }).limit(1);
    const newId = (lastReview[0]?.id || 0) + 1;

    const review = new Reviews({
      id: newId,
      name: data['name'],
      dealership: data['dealership'],
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    });
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// === Start the Express server ===
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
