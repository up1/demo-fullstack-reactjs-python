import React, { useState } from "react";
import TrackingForm from "./components/TrackingForm";
import TrackingResults from "./components/TrackingResults";

const appStyle = {
  maxWidth: "700px",
  margin: "40px auto",
  padding: "0 20px",
  fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
};

const headerStyle = {
  textAlign: "center",
  color: "#2c3e50",
  marginBottom: "30px",
};

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (itemNumbers) => {
    setLoading(true);
    setError("");
    setResults([]);
    try {
      const response = await fetch("/api/track", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_numbers: itemNumbers }),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to fetch tracking info");
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={appStyle}>
      <h1 style={headerStyle}>Order Tracking</h1>
      <TrackingForm onSearch={handleSearch} loading={loading} />
      {error && (
        <p style={{ color: "red", textAlign: "center" }}>{error}</p>
      )}
      <TrackingResults results={results} />
    </div>
  );
}

export default App;
