export async function loginUser(email, password) {
  const resp = await fetch("http://localhost:5000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!resp.ok) throw new Error(await resp.text());
  return await resp.json(); // Expects {token: "..."}
}
export async function registerUser(username, email, password) {
  const resp = await fetch("http://localhost:5000/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });
  if (!resp.ok) throw new Error(await resp.text());
  // Adjust if your backend returns something different!
  return await resp.json(); // for success message, etc.
}
export async function getPredictionHistory() {
  const resp = await fetch("http://localhost:5000/api/predict/history", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("jwt")}`
    }
  });
  if (!resp.ok) throw new Error(await resp.text());
  return await resp.json();
}
export async function getUserProfile() {
  const resp = await fetch("http://localhost:5000/api/auth/me", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("jwt")}`
    }
  });
  if (!resp.ok) throw new Error(await resp.text());
  return await resp.json();
}

