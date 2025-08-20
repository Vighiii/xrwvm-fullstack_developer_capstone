/*jshint esversion: 8 */
import React, { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/review.png";
import Header from "../Header/Header";
import { Container, Row, Col, Card, Button } from "react-bootstrap";

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { dealerId } = useParams();

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("/dealer/"));
  const dealer_url = root_url + "/api/dealerships/" + dealerId;
  const reviews_url = root_url + "/api/dealerships/" + dealerId + "/reviews";
  const post_review = root_url + "/dealer/" + dealerId + "/review";

  const get_dealer = useCallback(async () => {
    try {
      const response = await fetch(dealer_url);
      if (!response.ok) {
        throw new Error("Failed to fetch dealer");
      }
      const data = await response.json();
      setDealer(data);
    } catch (err) {
      setError(err.message);
    }
  }, [dealer_url]);

  const get_reviews = useCallback(async () => {
    try {
      const response = await fetch(reviews_url);
      if (!response.ok) {
        throw new Error("Failed to fetch reviews");
      }
      const data = await response.json();
      setReviews(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [reviews_url]);

  const senti_icon = (sentiment) => {
    return sentiment === "positive" ? positive_icon :
           sentiment === "negative" ? negative_icon : neutral_icon;
  };

  useEffect(() => {
    const fetchData = async () => {
      await get_dealer();
      await get_reviews();
    };
    fetchData();
  }, [get_dealer, get_reviews]);

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

  if (error) {
    return (
      <div>
        <Header />
        <div className="error-container">
          <p>Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <Container className="mt-4">
        <Row>
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>{dealer.full_name}</Card.Title>
                <Card.Text>
                  <strong>Address:</strong> {dealer.address}<br />
                  <strong>City:</strong> {dealer.city}<br />
                  <strong>State:</strong> {dealer.state}<br />
                  <strong>Zip:</strong> {dealer.zip}
                </Card.Text>
                <Button
                  variant="primary"
                  onClick={() => navigate(post_review)}
                >
                  <img
                    src={review_icon}
                    alt="Review"
                    style={{ width: "20px", marginRight: "5px" }}
                  />
                  Write a Review
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col>
            <h3>Reviews</h3>
            {reviews.map((review) => (
              <Card key={review.id} className="mb-3">
                <Card.Body>
                  <div className="d-flex align-items-center mb-2">
                    <img
                      src={senti_icon(review.sentiment)}
                      alt={review.sentiment}
                      style={{ width: "24px", marginRight: "10px" }}
                    />
                    <Card.Title className="mb-0">{review.name}</Card.Title>
                  </div>
                  {review.purchase && (
                    <Card.Subtitle className="mb-2 text-muted">
                      Purchased: {review.car_make} {review.car_model} ({review.car_year})
                    </Card.Subtitle>
                  )}
                  <Card.Text>{review.review}</Card.Text>
                  <Card.Text className="text-muted">
                    <small>Posted on: {new Date(review.purchase_date).toLocaleDateString()}</small>
                  </Card.Text>
                </Card.Body>
              </Card>
            ))}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Dealer;
