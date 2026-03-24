import React, { useState } from "react";

const formStyle = {
  display: "flex",
  flexDirection: "column",
  gap: "12px",
  marginBottom: "24px",
};

const inputStyle = {
  padding: "12px",
  fontSize: "16px",
  border: "2px solid #3498db",
  borderRadius: "6px",
  outline: "none",
};

const buttonStyle = {
  padding: "12px",
  fontSize: "16px",
  backgroundColor: "#3498db",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  fontWeight: "bold",
};

const hintStyle = {
  fontSize: "13px",
  color: "#7f8c8d",
  margin: 0,
};

function TrackingForm({ onSearch, loading }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const items = input
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    if (items.length === 0) return;
    if (items.length > 10) {
      alert("A maximum of 10 items can be entered at a time");
      return;
    }
    onSearch(items);
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <input
        style={inputStyle}
        type="text"
        placeholder="Enter 13 digit item number (e.g. EF582568151TH)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <p style={hintStyle}>
        Use comma to separate multiple items (max 10). Sample:
        EF582621151TH, EA666458151TH, RG453678925TH
      </p>
      <button type="submit" style={buttonStyle} disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

export default TrackingForm;
