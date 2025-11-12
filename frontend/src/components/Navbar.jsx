import React from "react";
import logo from "../assets/LFlogo.png"; // Put your logo image in src/assets/

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm" style={{padding: "10px 30px"}}>
    <div className="container-fluid" style={{
      display: "flex", 
      alignItems: "center", 
      justifyContent: "space-between"
    }}>
      <a href="/" className="navbar-brand d-flex align-items-center" style={{gap: "10px"}}>
        <img src={logo} alt="Logo" style={{ width: 38, height: 38 }} />
        <span style={{ fontWeight: 600, fontSize: 22, letterSpacing: 1 }}>Load Forecaster</span>
      </a>
      <div style={{
        display: "flex", gap: "28px", alignItems: "center", fontSize: 18
      }}>
        <a className="nav-link" href="/forecast">Forecast</a>
        <a className="nav-link" href="/dashboard">Dashboard</a>
        <a className="nav-link" href="/login">Login/Register</a>
        <a className="nav-link" href="/profile">Profile</a>
      </div>
    </div>
  </nav>
);

export default Navbar;
