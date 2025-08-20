/*jshint esversion: 8 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './Dealers.css';
import './PostReview.css';
import '../assets/style.css';
import Header from '../Header/Header';
import { Form, Button, Alert } from 'react-bootstrap';

const PostReview = () => {
  const [review, setReview] = useState({
    name: '',
    purchase: false,
    purchase_date: '',
    car_make: '',
    car_model: '',
    car_year: '',
    review: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const { dealerId } = useParams();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setReview((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate required fields
      if (!review.name || !review.review) {
        throw new Error('Name and review are required');
      }

      if (review.purchase) {
        if (!review.purchase_date || !review.car_make || !review.car_model || !review.car_year) {
          throw new Error('All car details are required when purchase is checked');
        }

        // Validate car year
        const year = parseInt(review.car_year, 10);
        if (Number.isNaN(year) || year < 1900 || year > new Date().getFullYear()) {
          throw new Error('Please enter a valid car year');
        }
      }

      // Validate review length
      if (review.review.length < 10) {
        throw new Error('Review must be at least 10 characters long');
      }

      const response = await fetch(`/api/dealerships/${dealerId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(review),
      });

      if (!response.ok) {
        throw new Error('Failed to submit review');
      }

      setSuccess(true);
      setReview({
        name: '',
        purchase: false,
        purchase_date: '',
        car_make: '',
        car_model: '',
        car_year: '',
        review: '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div>
        <Header />
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <div className="container mt-5">
        <h2>Post a Review</h2>
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">Review submitted successfully!</Alert>}
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={review.name}
              onChange={handleChange}
              required
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Check
              type="checkbox"
              name="purchase"
              label="I purchased a car from this dealer"
              checked={review.purchase}
              onChange={handleChange}
            />
          </Form.Group>
          {review.purchase && (
            <>
              <Form.Group className="mb-3">
                <Form.Label>Purchase Date</Form.Label>
                <Form.Control
                  type="date"
                  name="purchase_date"
                  value={review.purchase_date}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Car Make</Form.Label>
                <Form.Control
                  type="text"
                  name="car_make"
                  value={review.car_make}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Car Model</Form.Label>
                <Form.Control
                  type="text"
                  name="car_model"
                  value={review.car_model}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Car Year</Form.Label>
                <Form.Control
                  type="number"
                  name="car_year"
                  value={review.car_year}
                  onChange={handleChange}
                  min="1900"
                  max={new Date().getFullYear()}
                  required
                />
              </Form.Group>
            </>
          )}
          <Form.Group className="mb-3">
            <Form.Label>Review</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              name="review"
              value={review.review}
              onChange={handleChange}
              required
            />
          </Form.Group>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Review'}
          </Button>
        </Form>
      </div>
    </div>
  );
};

export default PostReview;