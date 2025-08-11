import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
    const [dealersList, setDealersList] = useState([]);
    const [states, setStates] = useState([]);
    const [selectedState, setSelectedState] = useState('All'); // New state to manage the selected filter value

    // Function to fetch dealerships based on the selected state
    const fetchDealerships = async (stateParam) => { // Renamed parameter to avoid conflict with useState
      let url = `/djangoapp/get_dealers`;
      if (stateParam && stateParam !== 'All') {
        url = `/djangoapp/get_dealers/${stateParam}`; // Correctly form URL for specific state
      }

      try {
        const res = await fetch(url, {
          method: "GET"
        });
        const retobj = await res.json();
        if (retobj.status === 200) {
          setDealersList(Array.from(retobj.dealers));
        } else {
          console.error("Failed to fetch dealerships:", retobj.message);
          setDealersList([]); // Clear list on error
        }
      } catch (error) {
        console.error("Network error fetching dealerships:", error);
        setDealersList([]); // Clear list on network error
      }
    };

    // Function to get all dealers and populate states dropdown initially
    const get_all_dealers_and_states = async () => {
      const res = await fetch("/djangoapp/get_dealers", { // Always fetch all initially to get states
        method: "GET"
      });
      const retobj = await res.json();
      if (retobj.status === 200) {
        let all_dealers = Array.from(retobj.dealers);
        let uniqueStates = new Set();
        all_dealers.forEach((dealer) => {
          uniqueStates.add(dealer.state);
        });
        setStates(Array.from(uniqueStates)); // Set unique states for the dropdown
        setDealersList(all_dealers); // Set the initial list of all dealers
      } else {
        console.error("Failed to fetch initial dealerships and states:", retobj.message);
      }
    };

    // Use useEffect to fetch initial data and then re-fetch when selectedState changes
    useEffect(() => {
      // On initial mount, get all dealers and populate states
      get_all_dealers_and_states();
    }, []); // Empty dependency array: runs only once on component mount

    // This useEffect watches for changes in selectedState and fetches dealers accordingly
    useEffect(() => {
      if (selectedState) { // Ensure selectedState is not null/undefined
        fetchDealerships(selectedState);
      }
    }, [selectedState]); // Dependency array: re-run when selectedState changes

    const handleStateChange = (e) => {
      setSelectedState(e.target.value); // Update the selectedState
    };

    let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
return (
    <div>
      <Header />

      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={handleStateChange} value={selectedState}> {/* Use handleStateChange and value */}
                <option value="All">All States</option> {/* Set value to "All" for initial display */}
                {states.map(state => (
                  <option key={state} value={state}>{state}</option> // Add key for list items
                ))}
              </select>
            </th>
            {isLoggedIn ? (
              <th>Review Dealer</th>
            ) : <></>
            }
          </tr>
        </thead>
        <tbody>
          {dealersList.length === 0 ? (
            <tr><td colSpan="7">Loading dealerships...</td></tr>
          ) : (
            dealersList.map(dealer => (
              <tr key={dealer.id}> {/* Add key for list items */}
                <td>{dealer['id']}</td>
                <td><a href={'/dealer/' + dealer['id']}>{dealer['full_name']}</a></td>
                <td>{dealer['city']}</td>
                <td>{dealer['address']}</td>
                <td>{dealer['zip']}</td>
                <td>{dealer['state']}</td>
                {isLoggedIn ? (
                  <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>
                ) : <></>
                }
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers;