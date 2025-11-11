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
