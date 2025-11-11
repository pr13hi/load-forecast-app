import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import ErrorAlert from "../components/ErrorAlert";
import { FormInput } from "../components/FormInput";
import { loginUser } from "../utils/api";
import { saveToken } from "../utils/auth";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
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
      const resp = await loginUser(form.email, form.password);
      saveToken(resp.token);
      setLoading(false);
      navigate("/dashboard");
    } catch (err) {
      setLoading(false);
      setError("Login failed: " + (err.message || "Check your credentials"));
    }
  }

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: "420px", margin: "60px auto" }}>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
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
          <button type="submit" className="btn btn-primary w-100" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        {error && <ErrorAlert message={error} />}
        <div style={{ marginTop: "1em", textAlign: "center" }}>
          <span>
            Don't have an account?
            <a href="/register" style={{ marginLeft: "7px" }}>Register</a>
          </span>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Login;
