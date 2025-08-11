/*jshint esversion: 8 */ // This line should already be at the top from previous fixes.

const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors'); // Corrected spacing
const app = express(); // Added semicolon
const port = 3030;

app.use(cors()); // Added semicolon
app.use(require('body-parser').urlencoded({ extended: false })); // Added semicolon

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8')); // Added semicolon
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8')); // Added semicolon

mongoose.connect("mongodb://mongo_db:27017/", {'dbName': 'dealershipsDB'}); // Added semicolon and fixed spacing

const Reviews = require('./review'); // Added semicolon

const Dealerships = require('./dealership'); // Added semicolon

try {
    Reviews.deleteMany({}).then(() => {
        Reviews.insertMany(reviews_data.reviews); // Fixed to dot notation: reviews_data['reviews'] -> reviews_data.reviews
    });
    Dealerships.deleteMany({}).then(() => {
        Dealerships.insertMany(dealerships_data.dealerships); // Fixed to dot notation: dealerships_data['dealerships'] -> dealerships_data.dealerships
    });

} catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
}


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API"); // Added semicolon
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const documents = await Reviews.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const documents = await Reviews.find({ dealership: req.params.id });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const documents = await Dealerships.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {

});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
    //Write your code here
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
    data = JSON.parse(req.body); // Added semicolon
    const documents = await Reviews.find().sort({ id: -1 }); // Added semicolon
    let new_id = documents[0].id + 1; // Fixed to dot notation: documents[0]['id'] -> documents[0].id

    const review = new Reviews({
        "id": new_id,
        "name": data.name,
        "dealership": data.dealership,
        "review": data.review,
        "purchase": data.purchase,
        "purchase_date": data.purchase_date,
        "car_make": data.car_make,
        "car_model": data.car_model,
        "car_year": data.car_year
    });

    try {
        const savedReview = await review.save();
        res.json(savedReview);
    } catch (error) {
        console.log(error); // Added semicolon
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
