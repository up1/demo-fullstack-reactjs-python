import React from "react";

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "20px",
};

const thStyle = {
  backgroundColor: "#3498db",
  color: "white",
  padding: "12px",
  textAlign: "left",
};

const tdStyle = {
  padding: "12px",
  borderBottom: "1px solid #ecf0f1",
};

function TrackingResults({ results }) {
  if (results.length === 0) return null;

  return (
    <table style={tableStyle}>
      <thead>
        <tr>
          <th style={thStyle}>Item Number</th>
          <th style={thStyle}>Status</th>
          <th style={thStyle}>Location</th>
          <th style={thStyle}>Last Updated</th>
        </tr>
      </thead>
      <tbody>
        {results.map((item) => (
          <tr key={item.item_number}>
            <td style={tdStyle}>{item.item_number}</td>
            <td style={tdStyle}>{item.status}</td>
            <td style={tdStyle}>{item.location || "-"}</td>
            <td style={tdStyle}>
              {new Date(item.updated_at).toLocaleString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TrackingResults;
