import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  const rootUrl = window.location.origin;
  const dealerUrl = `${rootUrl}/djangoapp/dealer/${id}`;
  const reviewUrl = `${rootUrl}/djangoapp/add_review`;
  const carModelsUrl = `${rootUrl}/djangoapp/get_cars`;

  const postReview = async () => {
    let name = `${sessionStorage.getItem("firstname")} ${sessionStorage.getItem("lastname")}`;
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    if (!model || !review || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    const [makeChosen, modelChosen] = model.split(" ");

    const jsonInput = JSON.stringify({
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: makeChosen,
      car_model: modelChosen,
      car_year: year,
    });

    try {
      const res = await fetch(reviewUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonInput,
      });

      const json = await res.json();
      if (json.status === 200) {
        window.location.href = `${rootUrl}/dealer/${id}`;
      } else {
        alert("Failed to post review.");
      }
    } catch (error) {
      console.error("Error posting review:", error);
      alert("An error occurred while posting the review.");
    }
  };

  const getDealer = async () => {
    try {
      const res = await fetch(dealerUrl);
      const retObj = await res.json();

      if (retObj.status === 200 && retObj.dealer.length > 0) {
        setDealer(retObj.dealer[0]);
      } else {
        console.error("Dealer not found.");
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
    }
  };

  const getCars = async () => {
    try {
      const res = await fetch(carModelsUrl);
      const retObj = await res.json();
      setCarmodels(retObj.CarModels || []);
    } catch (error) {
      console.error("Error fetching car models:", error);
    }
  };

  useEffect(() => {
    getDealer();
    getCars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea
          id="review"
          cols="50"
          rows="7"
          placeholder="Write your review here..."
          onChange={(e) => setReview(e.target.value)}
        ></textarea>

        <div className="input_field">
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className="input_field">
          Car Make & Model
          <select
            name="cars"
            id="cars"
            defaultValue=""
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled hidden>
              Choose Car Make and Model
            </option>
            {carmodels.map((carmodel, index) => (
              <option key={index} value={`${carmodel.CarMake} ${carmodel.CarModel}`}>
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year
          <input
            type="number"
            onChange={(e) => setYear(e.target.value)}
            max={2023}
            min={2015}
            placeholder="Enter Year"
          />
        </div>

        <div>
          <button className="postreview" onClick={postReview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
