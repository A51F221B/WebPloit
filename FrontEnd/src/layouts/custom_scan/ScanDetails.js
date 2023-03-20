import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

function ScanDetails({ results }) {
  if (!results) {
    return null;
  }

  if (results.data === "No Vulnerability Found") {
    return (
      <Box sx={{ mt: 3, p: 2, bgcolor: "success.light", borderRadius: 1 }}>
        <Typography variant="h6" gutterBottom>
          Scan Details
        </Typography>
        <Typography variant="body1">No vulnerability found.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Scan Details
      </Typography>
      {results.data.map((detail, index) => (
        <Box
          key={index}
          sx={{
            mt: 2,
            p: 2,
            borderRadius: 1,
            bgcolor: detail.status === 200 ? "success.light" : "error.light",
          }}
        >
          <Typography variant="body1" fontWeight="bold">
            {detail.part ? `Part: ${detail.part}` : ""}
          </Typography>
          <Typography variant="body1" fontWeight="bold">
            {detail.matchtype ? `Match Type: ${detail.matchtype}` : ""}
          </Typography>
          <Typography variant="body1" fontWeight="bold">
            {detail.payload ? `Payload: ${detail.payload}` : ""}
          </Typography>
          <Typography variant="body1" fontWeight="bold">
            {detail.url ? `URL: ${detail.url}` : ""}
          </Typography>
          <Typography variant="body1" fontWeight="bold">
            {detail.status ? `Status: ${detail.status}` : ""}
          </Typography>
        </Box>
      ))}
    </Box>
  );
}

export default ScanDetails;
