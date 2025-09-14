import PostReview from "./components/Dealers/PostReview"
import Dealers from './components/Dealers/Dealers'
import LoginPanel from "./components/Login/Login"
import RegisterPanel from "./components/Register/Register"
import { Routes, Route } from "react-router-dom"


function App() {
  return (
    <Routes>
    
      <Route path="/postreview/:id" element={<PostReview/>} />
      <Route path="/dealers/:id" element={<Dealers/>} />
      <Route path="/dealers" element={<Dealers/>} />  
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPanel />} />
    </Routes>
  );
}
export default App;
