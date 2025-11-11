import React from "react";

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
    <div className="container">
      <a className="navbar-brand" href="/">Load Forecaster</a>
      <div>
        <a className="nav-link" href="/forecast">Forecast</a>
        <a className="nav-link" href="/dashboard">Dashboard</a>
        <a className="nav-link" href="/login">Login</a>
        <a className="nav-link" href="/register">Register</a>
      </div>
    </div>
  </nav>
);

export default Navbar;
