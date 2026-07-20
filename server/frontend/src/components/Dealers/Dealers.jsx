import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"
// import PostReview from "./components/Dealers/PostReview"


const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  const dealer_url = `${window.location.origin}/djangoapp/get_dealers/`;

  const filterDealers = async (state) => {
    if (state === "All") {
      get_dealers();
      return;
    }
  
    const res = await fetch(`/djangoapp/get_dealers/${state}`, {
      method: "GET",
    });
  
    const retobj = await res.json();
    if (retobj.status === 200) {
      setDealersList(Array.isArray(retobj.dealers) ? retobj.dealers : []);
    }
  };


  const get_dealers = async () => {
    const res = await fetch(dealer_url, { method: "GET" });
    const retobj = await res.json();
  
    if (retobj.status === 200) {
      const all_dealers = Array.isArray(retobj.dealers) ? retobj.dealers : [];
      const statesList = all_dealers
        .map((dealer) => dealer.state)
        .filter(Boolean);
  
      setStates(Array.from(new Set(statesList)));
      setDealersList(all_dealers);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;

  return (
    <div>
      <Header />

      <table className='table'>
        <tr>
          <th>ID</th>
          <th>Dealer Name</th>
          <th>City</th>
          <th>Address</th>
          <th>Zip</th>
          <th>
            <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
              <option value="" disabled hidden>State</option>
              <option value="All">All States</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </th>
          {isLoggedIn ? <th>Review Dealer</th> : <></>}
        </tr>

        {dealersList.map(dealer => (
          <tr key={dealer['id']}>
            <td>{dealer['id']}</td>
            <td><a href={'/dealer/' + dealer['id']}>{dealer['full_name']}</a></td>
            <td>{dealer['city']}</td>
            <td>{dealer['address']}</td>
            <td>{dealer['zip']}</td>
            <td>{dealer['state']}</td>
            {isLoggedIn ? (
              <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>
            ) : <></>}
          </tr>
        ))}
      </table>
    </div>
  )
}

export default Dealers