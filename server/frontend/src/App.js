// frontend/src/App.js

import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register"; // Assuming Register is the default export
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      {/* Route for the Login page */}
      <Route path="/login" element={<LoginPanel />} />
      {/* Route for the Register page */}
      <Route path="/register" element={<Register/>}/>
    </Routes>
  );
}
export default App