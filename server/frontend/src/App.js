import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer";
// استيراد مكون إضافة المراجعة - تأكد من مطابقة الاسم والمسار لديك في مجلد components
import PostReview from "./components/Dealers/PostReview"; 

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      
      {/* هذا المسار هو الذي يحميك من الشاشة البيضاء عند الدخول لصفحة إضافة مراجعة */}
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;