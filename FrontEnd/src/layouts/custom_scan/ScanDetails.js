import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { CSVLink } from "react-csv";
import MDButton from "components/MDButton";
import jsPDF from "jspdf";
import "jspdf-autotable";

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

  const exportPDF = () => {
    const doc = new jsPDF();
    const tableRows = results.data.map((detail) => {
      return [
        detail.part ? `Part: ${detail.part}` : "",
        detail.matchtype ? `Match Type: ${detail.matchtype}` : "",
        detail.payload ? `Payload: ${detail.payload}` : "",
        detail.url ? `URL: ${detail.url}` : "",
        detail.status ? `Status: ${detail.status}` : "",
      ];
    });
  
    // custom styles for each column
    const styles = {
      0: { columnWidth: 70 },
      1: { columnWidth: 80 },
      2: { columnWidth: 50 },
      3: { columnWidth: 15 },
      4: { columnWidth: 40 },
    };
    
    doc.autoTable({
      head: [["Part", "Match Type", "Payload", "URL", "Status"]],
      body: tableRows,
      styles, // pass the styles object as an option
    });
    doc.save("scan_results.pdf");
  };
  
  

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Scan Details
      </Typography>
          <Box sx={{ mb: 2 }}>
      <CSVLink
        data={results.data}
        filename="scan_results.csv"
        style={{ marginRight: "8px" }}
      >
        <MDButton variant="contained" color="primary" size="small">
          Export to CSV
        </MDButton>
      </CSVLink>
      <MDButton
        variant="contained"
        color="primary"
        size="small"
        onClick={exportPDF}
      >
        Export to PDF
      </MDButton>
    </Box>

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
