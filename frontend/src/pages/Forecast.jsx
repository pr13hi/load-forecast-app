import React, { useState } from "react";
import { Container, Form, Button, Alert, Card } from "react-bootstrap";

function Forecast() {
  const [form, setForm] = useState({
    temperature: "",
    hour: "",
    date: ""
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjI0NTY3OCwianRpIjoiM2UzZWJlNTQtNDkxZi00YzQxLTk4OTQtYjU3YWQ0ODc2NjNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NjIyNDU2NzgsImNzcmYiOiJlMjk1NzY4MC1mMzAzLTRjOWUtODdjMS0zNGE1MmRmY2Y0MWUiLCJleHAiOjE3NjQ4Mzc2Nzh9.WOuG5zsL1qDbTVDX08DsRvcp6fAbZF8zK02TInJDeL0";

  function handleChange(e) {
    let { name, value } = e.target;
    if (name === "date") {
      if (/^\d{2}-\d{2}-\d{4}$/.test(value)) {
        const [dd, mm, yyyy] = value.split("-");
        value = `${yyyy}-${mm}-${dd}`;
      }
    }
    setForm({
      ...form,
      [name]: value
    });
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
    } catch (err) {
      setError(String(err));
    }
  }

  return (
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
  );
}

export default Forecast;
