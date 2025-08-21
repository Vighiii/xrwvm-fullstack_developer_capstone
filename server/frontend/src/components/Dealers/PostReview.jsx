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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const params = useParams();
  const id = params.id;

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));
  let dealer_url = `${root_url}djangoapp/dealer/${id}`;
  let review_url = `${root_url}djangoapp/add_review`;
  let carmodels_url = `${root_url}djangoapp/get_cars`;

  const postReview = async () => {
    setLoading(true);
    setError(null);

    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    if (!model || review === "" || date === "" || year === "") {
      setError("All details are mandatory");
      setLoading(false);
      return;
    }

    let modelSplit = model.split(" ");
    let makeChosen = modelSplit[0];
    let modelChosen = modelSplit.length > 1 ? modelSplit[1] : "";

    let jsonInput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": makeChosen,
      "car_model": modelChosen,
      "car_year": year,
    });

    try {
      const response = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsonInput,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const json = await response.json();
      if (json.status === 200) {
        window.location.href = `${window.location.origin}/dealer/${id}`;
      } else {
        setError("Failed to post review");
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  const getDealer = async () => {
    try {
      const response = await fetch(dealer_url, {
        method: "GET"
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const retObj = await response.json();

      if (retObj.status === 200) {
        let dealerObjs = Array.from(retObj.dealer)
        if (dealerObjs.length > 0) {
          setDealer(dealerObjs[0])
        }
      }
    } catch (error) {
      setError(error.message);
    }
  }

  const getCars = async () => {
    try {
      const response = await fetch(carmodels_url, {
        method: "GET"
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const retObj = await response.json();

      let carModelsArr = Array.from(retObj.CarModels)
      setCarmodels(carModelsArr)
    } catch (error) {
      setError(error.message);
    }
  }

  useEffect(() => {
    getDealer();
    getCars();
  }, [id]);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
        <div className='input_field'>
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>
        <div className='input_field'>
          Car Make
          <select name="cars" id="cars" onChange={(e) => setModel(e.target.value)}>
            <option value="" selected disabled hidden>Choose Car Make and Model</option>
            {carmodels.map(carmodel => (
              <option value={carmodel.CarMake + " " + carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
            ))}
          </select>
        </div>

        <div className='input_field'>
          Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015} />
        </div>

        <div>
          <button className='postreview' onClick={postReview} disabled={loading}>
            {loading ? "Posting..." : "Post Review"}
          </button>
          {error && <div style={{ color: 'red' }}>{error}</div>}
        </div>
      </div>
    </div>
  )
}
export default PostReview;
