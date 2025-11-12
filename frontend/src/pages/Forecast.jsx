import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Container, Form, Button, Alert, Card } from "react-bootstrap";

function Forecast() {
  const [form, setForm] = useState({ temperature: "", hour: "", date: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const JWT = localStorage.getItem("jwt");

  function handleChange(e) {
    let { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(form.date)) {
      setError("Please use the date picker or enter date as YYYY-MM-DD.");
      return;
    }
    try {
      const resp = await fetch("http://localhost:5000/api/predict/single", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${JWT}`
        },
        body: JSON.stringify(form)
      });
      if (!resp.ok) throw new Error(await resp.text());
      const data = await resp.json();
      setResult(data);
      // Optionally redirect to dashboard so you always see history update:
      navigate("/dashboard");
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <>
      <Navbar />
      <Container style={{ maxWidth: 500, marginTop: 40 }}>
        <Card>
          <Card.Body>
            <Card.Title>Electric Load Forecaster</Card.Title>
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="temperature">
                <Form.Label>Temperature (°C)</Form.Label>
                <Form.Control
                  type="number"
                  name="temperature"
                  required
                  value={form.temperature}
                  onChange={handleChange}
                  step="0.1"
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="hour">
                <Form.Label>Hour (0-23)</Form.Label>
                <Form.Control
                  type="number"
                  name="hour"
                  min={0}
                  max={23}
                  required
                  value={form.hour}
                  onChange={handleChange}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="date">
                <Form.Label>Date</Form.Label>
                <Form.Control
                  type="date"
                  name="date"
                  required
                  value={form.date}
                  onChange={handleChange}
                />
              </Form.Group>
              <Button variant="primary" type="submit">Get Prediction</Button>
            </Form>
            {result &&
              <Alert className="mt-3" variant="success">
                <strong>Predicted Load:</strong> {result.predicted_load}<br />
                <strong>Lower Bound:</strong> {result.lower_bound}<br />
                <strong>Upper Bound:</strong> {result.upper_bound}<br />
                <strong>Interval:</strong> {result.confidence_interval}
              </Alert>
            }
            {error && <Alert className="mt-3" variant="danger">{error}</Alert>}
          </Card.Body>
        </Card>
      </Container>
      <Footer />
    </>
  );
}

export default Forecast;
