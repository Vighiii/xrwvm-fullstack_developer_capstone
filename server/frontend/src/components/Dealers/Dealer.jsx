import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positiveIcon from "../assets/positive.png";
import neutralIcon from "../assets/neutral.png";
import negativeIcon from "../assets/negative.png";
import reviewIcon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(null);

  let { id } = useParams();
  let rootUrl = window.location.origin;
  let dealerUrl = `${rootUrl}/djangoapp/dealer/${id}`;
  let reviewsUrl = `${rootUrl}/djangoapp/reviews/dealer/${id}`;
  let postReviewUrl = `${rootUrl}/postreview/${id}`;

  const getDealer = async () => {
    try {
      const response = await fetch(dealerUrl);
      const data = await response.json();
      if (data.status === 200) {
        setDealer(data.dealer[0]);
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
    }
  };

  const getReviews = async () => {
    try {
      const response = await fetch(reviewsUrl);
      const data = await response.json();
      if (data.status === 200) {
        if (data.reviews.length > 0) {
          setReviews(data.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const getSentiIcon = (sentiment) => {
    if (sentiment === "positive") {
      return positiveIcon;
    } else if (sentiment === "negative") {
      return negativeIcon;
    } else {
      return neutralIcon;
    }
  };

  useEffect(() => {
    getDealer();
    getReviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(<a href={postReviewUrl}><img src={reviewIcon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' /></a>);
    }
  }, [id]); // Added id as a dependency to trigger useEffect when id changes

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>{dealer.full_name}{postReview}</h1>
        <h4 style={{ color: "grey" }}>{dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}</h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <div>Loading Reviews....</div>
        ) : unreviewed ? <div>No reviews yet!</div> :
          reviews.map((review, index) => (
            <div key={index} className='review_panel'>
              <img src={getSentiIcon(review.sentiment)} className="emotion_icon" alt='Sentiment' />
              <div className='review'>{review.review}</div>
              <div className="reviewer">{review.name} {review.car_make} {review.car_model} {review.car_year}</div>
            </div>
          ))}
      </div>
    </div>
  );
}

export default Dealer;

