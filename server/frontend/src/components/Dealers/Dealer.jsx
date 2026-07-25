import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import Header from "../Header/Header";
import negativeIcon from "../../assets/negative.png";
import neutralIcon from "../../assets/neutral.png";
import positiveIcon from "../../assets/positive.png";
import "./Dealers.css";

const sentimentIcon = (sentiment) => {
  if (sentiment === "positive") return positiveIcon;
  if (sentiment === "negative") return negativeIcon;
  return neutralIcon;
};

const Dealer = () => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const isLoggedIn = Boolean(sessionStorage.getItem("username"));

  useEffect(() => {
    const loadDealer = async () => {
      setLoading(true);
      setError("");
      try {
        const [dealerResponse, reviewsResponse] = await Promise.all([
          fetch(`/djangoapp/dealer/${id}`),
          fetch(`/djangoapp/reviews/dealer/${id}`),
        ]);
        const dealerData = await dealerResponse.json();
        const reviewsData = await reviewsResponse.json();

        if (!dealerResponse.ok || !dealerData.dealer?.length) {
          throw new Error("Dealer not found.");
        }

        setDealer(dealerData.dealer[0]);
        setReviews(Array.isArray(reviewsData.reviews) ? reviewsData.reviews : []);
      } catch (requestError) {
        setError(requestError.message || "Could not load dealer details.");
      } finally {
        setLoading(false);
      }
    };

    loadDealer();
  }, [id]);

  return (
    <div className="page-shell">
      <Header />
      <main className="content">
        {loading && <div className="loading">Loading dealer details…</div>}
        {error && <div className="error-message">{error}</div>}

        {dealer && (
          <>
            <section className="dealer-hero">
              <div>
                <p className="eyebrow">Dealer #{dealer.id}</p>
                <h1>{dealer.full_name}</h1>
                <p>
                  {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}
                </p>
              </div>
              {isLoggedIn ? (
                <Link className="primary-button" to={`/postreview/${id}`}>
                  Review Dealer
                </Link>
              ) : (
                <Link className="primary-button" to="/login">
                  Login to review
                </Link>
              )}
            </section>

            <section>
              <h2>Customer reviews</h2>
              {reviews.length === 0 ? (
                <div className="empty-state">No reviews yet.</div>
              ) : (
                <div className="reviews-grid">
                  {reviews.map((review) => (
                    <article className="review-card" key={review.id}>
                      <img
                        className="sentiment-icon"
                        src={sentimentIcon(review.sentiment)}
                        alt={`${review.sentiment || "neutral"} sentiment`}
                      />
                      <blockquote>{review.review}</blockquote>
                      <p className="reviewer">{review.name}</p>
                      <p className="vehicle">
                        {review.car_year} {review.car_make} {review.car_model}
                      </p>
                      <p className="purchase-date">Purchased: {review.purchase_date}</p>
                    </article>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
};

export default Dealer;
