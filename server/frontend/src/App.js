// src/App.js

import { Routes, Route } from "react-router-dom";
// Corrected import for Login/LoginPanel - assuming LoginPanel is what you want to use for /login
import LoginPanel from "./components/Login/Login"; // This imports the default export from Login.js as LoginPanel
import Register from "./components/Register/Register";
import Dealers from './components/Dealers/Dealers';

// **** THESE ARE THE MISSING IMPORTS THAT ARE CAUSING THE ESLINT ERRORS ****
// You need to import these components from their respective files.
// Adjust the paths based on where these component files actually live in your project.
// Common assumption: each component has its own folder within `src/components/`
import Home from './components/Home/Home'; // Assuming your Home component is in src/components/Home/Home.js
import Dealer from './components/Dealers/Dealer'; // Assuming your Dealer component is in src/components/Dealer/Dealer.js
 // Assuming PostReview is in src/components/PostReview/PostReview.js
import Header from './components/Header/Header';
import PostReview from "./components/Dealers/PostReview"

function App() {
  return (
    <Routes>
       <Route />
      <Route path="/" element={<Home />} />
      {/* If LoginPanel is the component for your login page, use it here: */}
      <Route path="/login" element={<LoginPanel />} />
      {/* If you have a separate component named 'Login' that is *not* LoginPanel,
          then you would need to import 'Login' as well: import Login from './components/Login/LoginComponent';
          But typically, LoginPanel IS the Login component.
      */}
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview/>} />
     
    </Routes>
  );
}
export default App;
