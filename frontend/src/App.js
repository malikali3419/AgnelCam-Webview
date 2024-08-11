import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/Login";
import CameraList from "./pages/CameraList";
import CameraView from "./pages/CameraView";
import VideoSegmentView from "./pages/VidoSegmentView";

import "./App.css";
// const PrivateRoute = ({ children }) => {
//   const token = localStorage.getItem("accessToken");
//   return token ? children : <Navigate to="/login" />;
// };

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/cameras" element={<CameraList />} />
        <Route path="/cameras/:id" element={<CameraView />} />
        <Route path="/segment/:id" element={<VideoSegmentView />} />

        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
