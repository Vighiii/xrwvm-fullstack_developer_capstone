import LoginPanel from "./components/Login/Login";
import RegistrationPanel from "./components/Register/Registration"; // Ensure this path is correct
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/registration" element={<RegistrationPanel />} /> {/* Added registration route */}
    </Routes>
  );
}

export default App;
