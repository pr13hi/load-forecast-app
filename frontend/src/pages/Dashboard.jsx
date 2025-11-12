import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Card, Button } from "react-bootstrap";
import { getPredictionHistory } from "../utils/api";

function PredictionHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getPredictionHistory()
      .then(data => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load prediction history");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading prediction history...</p>;
  if (error) return (
    <div style={{ color: "red", marginTop: "1em" }}>
      <h5>Prediction History</h5>
      Please <a href="/login">register or login</a> to view your prediction history.
    </div>
  );

  return (
    <div>
      <h3>Prediction History</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Date</th><th>Hour</th><th>Temp (°C)</th><th>Predicted Load</th><th>Lower</th><th>Upper</th>
          </tr>
        </thead>
        <tbody>
          {history.map((pred, idx) => (
            <tr key={idx}>
              <td>{pred.date}</td>
              <td>{pred.hour}</td>
              <td>{pred.temperature}</td>
              <td>{pred.predicted_load}</td>
              <td>{pred.lower_bound}</td>
              <td>{pred.upper_bound}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const Dashboard = () => {
  return (
    <>
      <Navbar />
      <div style={{ maxWidth: 700, margin: "60px auto" }}>
        <h2>Welcome to your Dashboard</h2>

        <div className="row mt-4" style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
          <Card style={{ flex: 1, minWidth: "250px" }}>
            <Card.Body>
              <Card.Title>Run a Prediction</Card.Title>
              <Card.Text>
                Get electric load forecasts with confidence intervals.
              </Card.Text>
              <Button href="/forecast" variant="primary">Go to Forecaster</Button>
            </Card.Body>
          </Card>

          <Card style={{ overflowX: "auto", maxWidth: "100%" }}>
            <Card.Body>
              <PredictionHistory />
            </Card.Body>
          </Card>

          <Card style={{ flex: 1, minWidth: "250px" }}>
            <Card.Body>
              <Card.Title>Profile & Settings</Card.Title>
              <Card.Text>
                View or update your profile information and preferences.
              </Card.Text>
              <Button href="/profile" variant="info">Go to Profile</Button>
            </Card.Body>
          </Card>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Dashboard;
