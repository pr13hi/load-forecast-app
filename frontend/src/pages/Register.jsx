import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import ErrorAlert from "../components/ErrorAlert";
import { FormInput } from "../components/FormInput";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../utils/api";

const Register = () => {
  const [form, setForm] = useState({ email: "", username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
  e.preventDefault();
  setError("");
  setLoading(true);
  try {
    await registerUser(form.username, form.email, form.password);
    setLoading(false);
    navigate("/login");
  } catch (err) {
    setLoading(false);
    setError("Registration failed: " + (err.message || "Try again"));
  }
}

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: "420px", margin: "60px auto" }}>
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <FormInput
            label="Username"
            name="username"
            type="text"
            value={form.username}
            onChange={handleChange}
            required
          />
          <FormInput
            label="Email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <FormInput
            label="Password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
          />
          <button type="submit" className="btn btn-success w-100" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        {error && <ErrorAlert message={error} />}
        <div style={{ marginTop: "1em", textAlign: "center" }}>
          <span>
            Already have an account?
            <a href="/login" style={{ marginLeft: "7px" }}>Login</a>
          </span>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Register;
