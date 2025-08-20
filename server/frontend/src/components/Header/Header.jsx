import React from 'react';
// Import custom styles and Bootstrap for styling
import "../assets/style.css";
import "../assets/bootstrap.min.css";

// Header component displays the navifation bar and login/logout elements
const Header = () => {

    // Async function to log out the current user
    const logout = async (e) => {
        // Prevent the default link click behavior
        e.preventDefault();
        
        // Build the logout URL using the current location's origin and a specific endpoint
        let logout_url = window.location.origin+"/djangoapp/logout";
        
        // Call the logout endpoint using a GET request
        const res = await fetch(logout_url, {
            method: "GET",
        });
    
        // Parse the response as JSON
        const json = await res.json();
        if (json) {
            // If the response is valid, get the username from session storage
            let username = sessionStorage.getItem('username');
            // Remove the username from session storage, effectively logging out the user
            sessionStorage.removeItem('username');
            // Redirect to the home page and reload to update the UI
            window.location.href = window.location.origin;
            window.location.reload();
            // Alert the user about the logout
            alert("Logging out "+username+"...")
        }
        else {
        // Alert if logout fails
        alert("The user could not be logged out.")
        }
  };
    
    //The default home page items are the login details panel
    let home_page_items =  <div></div>

    //Gets the username in the current session
    let curr_user = sessionStorage.getItem('username')

    //If the user is logged in, show the username and logout option on home page
    if ( curr_user !== null &&  curr_user !== "") {
        home_page_items = (
        <div className="input_panel">
            {/*Display the username */}
            <text className='username'>
                {sessionStorage.getItem("username")}
            </text>
            {/* Logout link that triggers the logout function */}
            <a className="nav_item" href="/djangoapp/logout" onClick={logout}>
                Logout
            </a>
        </div>
        );
    }

    // Render the Bootstrap-based navbar with navigation links and login/logout section
    return (
        <div>
          <nav class="navbar navbar-expand-lg navbar-light" style={{backgroundColor:"darkturquoise",height:"1in"}}>
            <div class="container-fluid">
              <h2 style={{paddingRight: "5%"}}>Dealerships</h2>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarText">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" style={{fontSize: "larger"}} aria-current="page" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style={{fontSize: "larger"}} href="/about">About Us</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style={{fontSize: "larger"}} href="/contact">Contact Us</a>
                    </li>
                </ul>
                <span class="navbar-text">
                  <div class="loginlink" id="loginlogout">
                  {home_page_items}
                  </div>
                  </span>
              </div>
            </div>
          </nav>
        </div>
    )
}

export default Header
