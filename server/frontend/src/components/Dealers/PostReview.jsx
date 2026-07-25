import { useEffect, useMemo, useState } from "react";
import { Navigate, useNavigate, useParams } from "react-router-dom";

import Header from "../Header/Header";
import "./Dealers.css";

const PostReview = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const username = sessionStorage.getItem("username");
  const [dealer, setDealer] = useState(null);
  const [cars, setCars] = useState([]);
  const [form, setForm] = useState({
    review: "",
    purchaseDate: "",
    car: "",
    carYear: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [dealerResponse, carsResponse] = await Promise.all([
          fetch(`/djangoapp/dealer/${id}`),
          fetch("/djangoapp/get_cars"),
        ]);
        const dealerData = await dealerResponse.json();
        const carsData = await carsResponse.json();
        setDealer(dealerData.dealer?.[0] || null);
        setCars(Array.isArray(carsData.CarModels) ? carsData.CarModels : []);
      } catch {
        setError("Could not load the review form.");
      }
    };
    loadData();
  }, [id]);

  const selectedCar = useMemo(
    () => cars.find((car) => `${car.CarMake}|${car.CarModel}` === form.car),
    [cars, form.car]
  );

  if (!username) {
    return <Navigate to="/login" replace />;
  }

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!selectedCar) {
      setError("Select a car make and model.");
      return;
    }

    setSubmitting(true);
    const firstName = sessionStorage.getItem("firstname") || "";
    const lastName = sessionStorage.getItem("lastname") || "";
    const fullName = `${firstName} ${lastName}`.trim() || username;

    try {
      const response = await fetch("/djangoapp/add_review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: fullName,
          dealership: Number(id),
          review: form.review,
          purchase: true,
          purchase_date: form.purchaseDate,
          car_make: selectedCar.CarMake,
          car_model: selectedCar.CarModel,
          car_year: Number(form.carYear),
        }),
      });
      const data = await response.json();
      if (!response.ok || data.status !== 200) {
        throw new Error(data.message || "Could not post the review.");
      }
      navigate(`/dealer/${id}`);
    } catch (requestError) {
      setError(requestError.message || "Could not post the review.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-shell">
      <Header />
      <main className="content review-form-wrap">
        <form className="review-form" onSubmit={handleSubmit}>
          <p className="eyebrow">Post a dealership review</p>
          <h1>{dealer?.full_name || "Dealer review"}</h1>
          <p>Complete all details, then take the required pre-submission screenshot.</p>

          {error && <div className="auth-error">{error}</div>}

          <label htmlFor="review-text">Review</label>
          <textarea
            id="review-text"
            name="review"
            rows="7"
            value={form.review}
            onChange={updateField}
            placeholder="Describe your dealership experience"
            required
          />

          <label htmlFor="purchase-date">Purchase Date</label>
          <input
            id="purchase-date"
            name="purchaseDate"
            type="date"
            value={form.purchaseDate}
            onChange={updateField}
            required
          />

          <label htmlFor="car-model">Car Make and Model</label>
          <select
            id="car-model"
            name="car"
            value={form.car}
            onChange={updateField}
            required
          >
            <option value="">Choose Car Make and Model</option>
            {cars.map((car) => (
              <option
                key={`${car.CarMake}-${car.CarModel}-${car.CarYear}`}
                value={`${car.CarMake}|${car.CarModel}`}
              >
                {car.CarMake} {car.CarModel}
              </option>
            ))}
          </select>

          <label htmlFor="car-year">Car Year</label>
          <input
            id="car-year"
            name="carYear"
            type="number"
            min="2015"
            max="2026"
            value={form.carYear}
            onChange={updateField}
            required
          />

          <button className="primary-button" type="submit" disabled={submitting}>
            {submitting ? "Posting…" : "Post Review"}
          </button>
        </form>
      </main>
    </div>
  );
};

export default PostReview;
