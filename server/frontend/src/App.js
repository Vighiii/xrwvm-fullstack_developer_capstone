import LoginPanel from "./components/Login/Login"
import RegisterPannel from "./components/Register/Register"
import Dealers from './components/Dealers/Dealers';
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPannel/>}></Route>
      <Route path="/dealers" element={<Dealers/>} />
    </Routes>
  );
}
export default App;
