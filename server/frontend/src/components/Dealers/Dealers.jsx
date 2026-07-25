import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

import Header from "../Header/Header";
import reviewIcon from "../../assets/reviewicon.png";
import "./Dealers.css";

const Dealers = () => {
  const [dealers, setDealers] = useState([]);
  const [allStates, setAllStates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();
  const selectedState = searchParams.get("state") || "All";
  const isLoggedIn = Boolean(sessionStorage.getItem("username"));

  useEffect(() => {
    const loadDealers = async () => {
      setLoading(true);
      setError("");
      try {
        const endpoint =
          selectedState === "All"
            ? "/djangoapp/get_dealers"
            : `/djangoapp/get_dealers/${encodeURIComponent(selectedState)}`;
        const response = await fetch(endpoint);
        const data = await response.json();
        if (!response.ok || data.status !== 200) {
          throw new Error("Could not load dealerships.");
        }
        setDealers(Array.isArray(data.dealers) ? data.dealers : []);
      } catch (requestError) {
        setError(requestError.message || "Could not load dealerships.");
      } finally {
        setLoading(false);
      }
    };

    loadDealers();
  }, [selectedState]);

  useEffect(() => {
    const loadStates = async () => {
      try {
        const response = await fetch("/djangoapp/get_dealers");
        const data = await response.json();
        const states = Array.from(
          new Set((data.dealers || []).map((dealer) => dealer.state).filter(Boolean))
        ).sort();
        setAllStates(states);
      } catch {
        setAllStates([]);
      }
    };
    loadStates();
  }, []);

  const title = useMemo(
    () => (selectedState === "All" ? "All dealerships" : `Dealerships in ${selectedState}`),
    [selectedState]
  );

  const handleStateChange = (event) => {
    const state = event.target.value;
    if (state === "All") {
      setSearchParams({});
    } else {
      setSearchParams({ state });
    }
  };

  return (
    <div className="page-shell">
      <Header />
      <main className="content">
        <section className="dealers-heading">
          <div>
            <p className="eyebrow">Best Cars network</p>
            <h1>{title}</h1>
            <p>Choose a dealer to view details and customer reviews.</p>
          </div>
          <label className="state-filter" htmlFor="state-filter">
            State
            <select
              id="state-filter"
              value={selectedState}
              onChange={handleStateChange}
            >
              <option value="All">All States</option>
              {allStates.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </label>
        </section>

        {loading && <div className="loading">Loading dealerships…</div>}
        {error && <div className="error-message">{error}</div>}

        {!loading && !error && (
          <div className="table-scroll">
            <table className="dealers-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Dealer Name</th>
                  <th>City</th>
                  <th>Address</th>
                  <th>Zip</th>
                  <th>State</th>
                  {isLoggedIn && <th>Review Dealer</th>}
                </tr>
              </thead>
              <tbody>
                {dealers.map((dealer) => (
                  <tr key={dealer.id}>
                    <td>{dealer.id}</td>
                    <td>
                      <Link to={`/dealer/${dealer.id}`}>{dealer.full_name}</Link>
                    </td>
                    <td>{dealer.city}</td>
                    <td>{dealer.address}</td>
                    <td>{dealer.zip}</td>
                    <td>{dealer.state}</td>
                    {isLoggedIn && (
                      <td>
                        <Link
                          className="review-action"
                          to={`/postreview/${dealer.id}`}
                          aria-label={`Review ${dealer.full_name}`}
                        >
                          <img src={reviewIcon} alt="" />
                          Review Dealer
                        </Link>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && !error && dealers.length === 0 && (
          <div className="empty-state">No dealerships match this state.</div>
        )}
      </main>
    </div>
  );
};

export default Dealers;
