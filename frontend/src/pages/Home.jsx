import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Home = () => (
  <>
    <Navbar />
    <div style={{ maxWidth: 600, margin: "60px auto", textAlign: "center" }}>
      <h1>Welcome to Load Forecaster!</h1>
      <p>
        Predict hourly electric loads using AI-powered models.<br />
        Sign in to access dashboards, batch uploads, and historical data.
      </p>
      <a href="/login" className="btn btn-primary" style={{ margin: "15px" }}>Login</a>
      <a href="/register" className="btn btn-outline-primary" style={{ margin: "15px" }}>Register</a>
    </div>
    <Footer />
  </>
);

export default Home;
