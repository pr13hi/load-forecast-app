import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    fetch("http://localhost:5000/api/auth/user-info", {
      headers: { Authorization: `Bearer ${jwt}` }
    })
      .then(res => res.ok ? res.json() : res.json().then(e => Promise.reject(e.error || "Failed")))
      .then(setUser)
      .catch(err => setError(typeof err === "string" ? err : "Could not load profile."));
  }, []);

  return (
  <>
    <Navbar />
    <div style={{ maxWidth: 480, margin: "60px auto" }}>
      <h2>Profile</h2>
      {error && (
        <div style={{ color: "red", marginTop: "1em" }}>
          Please <a href="/login">register or login</a> to access your profile.
        </div>
      )}
      {user ? (
        <div style={{fontSize: 18, lineHeight: 2}}>
          <div><b>Username:</b> {user.username}</div>
          <div><b>Email:</b> {user.email}</div>
          <div><b>Role:</b> {user.role}</div>
          <div><b>Verified:</b> {user.is_verified ? "Yes" : "No"}</div>
          <button
            style={{marginTop: 28, padding: "10px 24px", fontWeight: "bold"}}
            className="btn btn-outline-danger"
            onClick={() => {
              localStorage.removeItem("jwt");
              window.location = "/login";
            }}
          >Logout</button>
        </div>
      ) : !error && <div>Loading...</div>}
    </div>
  </>
);
}
