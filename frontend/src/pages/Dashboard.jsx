import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Card, Button } from "react-bootstrap";

const Dashboard = () => {
  // Later: Fetch stats, user info, recent predictions via API

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

          <Card style={{ flex: 1, minWidth: "250px" }}>
            <Card.Body>
              <Card.Title>Prediction History</Card.Title>
              <Card.Text>
                View your recent predictions, trends, and export data.
              </Card.Text>
              <Button href="/history" variant="secondary" disabled>Coming soon</Button>
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

        <div className="mt-5 text-center">
          <Button href="/feedback" variant="outline-success" disabled>Give Feedback (soon)</Button>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Dashboard;
