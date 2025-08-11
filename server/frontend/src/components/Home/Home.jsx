// /home/project/xrwvm-fullstack_developer_capstone/server/frontend/src/components/Home/Home.jsx

import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you have react-router-dom installed for navigation

function Home() {
  const containerStyle = {
    textAlign: 'center',
    padding: '50px',
    fontFamily: 'Arial, sans-serif',
  };

  const buttonContainerStyle = {
    marginTop: '30px',
  };

  const buttonStyle = {
    display: 'inline-block',
    margin: '10px',
    padding: '12px 25px',
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    textDecoration: 'none', // For Link components
  };

  const buttonHoverStyle = {
    backgroundColor: '#0056b3', // Darker blue on hover
  };

  return (
    <div style={containerStyle}>
      <h1>Welcome to Best Cars Dealership!</h1>
      <p>Your one-stop solution for finding the best car deals and managing your dealership network.</p>

      <div style={buttonContainerStyle}>
        {/* Login Button */}
        <Link to="/login" style={buttonStyle} onMouseOver={(e) => e.currentTarget.style.backgroundColor = buttonHoverStyle.backgroundColor} onMouseOut={(e) => e.currentTarget.style.backgroundColor = buttonStyle.backgroundColor}>
          Login
        </Link>

        {/* Register Button */}
        <Link to="/register" style={buttonStyle} onMouseOver={(e) => e.currentTarget.style.backgroundColor = buttonHoverStyle.backgroundColor} onMouseOut={(e) => e.currentTarget.style.backgroundColor = buttonStyle.backgroundColor}>
          Register
        </Link>

        {/* Dealers Button */}
        <Link to="/dealers" style={buttonStyle} onMouseOver={(e) => e.currentTarget.style.backgroundColor = buttonHoverStyle.backgroundColor} onMouseOut={(e) => e.currentTarget.style.backgroundColor = buttonStyle.backgroundColor}>
          View Dealerships
        </Link>
      </div>
    </div>
  );
}

export default Home;