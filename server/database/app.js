const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const Review = require('./models/review'); // Ajusta la ruta según tu estructura
const Dealer = require('./models/dealership'); // Ajusta la ruta según tu estructura

const app = express();
app.use(bodyParser.json());

// Endpoints

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const reviews = await Review.find();
        res.json(reviews);
    } catch (error) {
        res.status(500).send(error);
    }
});

// Fetch reviews by dealer ID
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const reviews = await Review.find({ dealerId: req.params.id });
        res.json(reviews);
    } catch (error) {
        res.status(500).send(error);
    }
});

// Fetch all dealers
app.get('/fetchDealers', async (req, res) => {
    try {
        const dealers = await Dealer.find();
        res.json(dealers);
    } catch (error) {
        res.status(500).send(error);
    }
});

// Fetch dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const dealers = await Dealer.find({ state: req.params.state });
        res.json(dealers);
    } catch (error) {
        res.status(500).send(error);
    }
});

// Fetch dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const dealer = await Dealer.findById(req.params.id);
        if (!dealer) {
            return res.status(404).send('Dealer not found');
        }
        res.json(dealer);
    } catch (error) {
        res.status(500).send(error);
    }
});

// Insert a review
app.post('/insert_review', async (req, res) => {
    const review = new Review(req.body);
    try {
        await review.save();
        res.status(201).send(review);
    } catch (error) {
        res.status(400).send(error);
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
