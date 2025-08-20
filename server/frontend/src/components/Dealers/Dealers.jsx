/*jshint esversion: 9 */
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Row, Col, Container, Button, Form } from "react-bootstrap";
import Dealer from "./Dealer";
import PostReview from "./PostReview";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";
import review_icon from "../assets/reviewicon.png";
import reviewIcon from '../assets/review.png';

const Dealers = () => {
  const [dealers, setDealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { state } = useParams();
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const navigate = useNavigate();

  const dealer_url = "/djangoapp/get_dealers";
  const dealer_url_by_state = "/djangoapp/get_dealers/";

  const filterDealers = async (state) => {
    const url = dealer_url_by_state + state;
    const res = await fetch(url, {
      method: "GET",
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      const state_dealers = Array.from(retobj.dealers);
      setDealersList(state_dealers);
    }
  };

  const get_dealers = async () => {
    const res = await fetch(dealer_url, {
      method: "GET",
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      const all_dealers = Array.from(retobj.dealers);
      const states = [];
      all_dealers.forEach((dealer) => {
        states.push(dealer.state);
      });

      setStates(Array.from(new Set(states)));
      setDealersList(all_dealers);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  useEffect(() => {
    const fetchDealers = async () => {
      try {
        const response = await fetch(
          `/api/dealerships/get_dealers?state=${state}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch dealers");
        }
        const data = await response.json();
        setDealers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDealers();
  }, [state]);

  if (loading) {
    return (
      <div>
        <Header />
        <div className='loading-container'>
          <div className='loading-spinner'></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Header />
        <div className='error-container'>
          <p>Error: {error}</p>
        </div>
      </div>
    );
  }

  const isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header />
      <Container className='mt-4'>
        <Row>
          <Col>
            <Form.Group className='mb-3'>
              <Form.Label>Filter by State</Form.Label>
              <Form.Select
                value={selectedState}
                onChange={(e) => {
                  setSelectedState(e.target.value);
                  if (e.target.value) {
                    filterDealers(e.target.value);
                  } else {
                    get_dealers();
                  }
                }}
              >
                <option value=''>All States</option>
                <option value='AL'>Alabama</option>
                <option value='AK'>Alaska</option>
                {/* Add more states as needed */}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>

        <Row>
          {dealers.map((dealer) => (
            <Col key={dealer.id} md={4} className='mb-4'>
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
                    variant='primary'
                    onClick={() => navigate(`/dealer/${dealer.id}`)}
                  >
                    <img
                      src={reviewIcon}
                      alt='Review'
                      style={{ width: '20px', marginRight: '5px' }}
                    />
                    View Reviews
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
      <PostReview />
      <table className="table">
        <tbody>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select
                name="state"
                id="state"
                onChange={(e) => filterDealers(e.target.value)}
              >
                <option value="" disabled hidden>
                  State
                </option>
                <option value="All">All States</option>
                {states.map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
          {dealersList.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td>
                <a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a>
              </td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td>
                  <a href={`/postreview/${dealer.id}`}>
                    <img
                      src={review_icon}
                      className="review_icon"
                      alt="Post Review"
                    />
                  </a>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;
