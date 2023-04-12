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

  if (results.vulnerability === false) {
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
    
    const tableRows = [
      ["Identity", results.identity || ""],
      ["Severity", results.severity || ""],
      ["Info", results.info || ""],
      ["URL", results.url || ""],
      ["Header Match", results.header_match !== undefined ? (results.header_match ? "Yes" : "No") : ""],
      ["Body Match", results.body_match !== undefined ? (results.body_match ? "Yes" : "No") : ""],
      ["Status Code Match", results.status_code_match !== undefined ? (results.status_code_match ? "Yes" : "No") : ""],
    ];

    doc.autoTable({
      theme: "grid",
      tableWidth: "wrap",
      body: tableRows,
    });

    doc.save("scan_results.pdf");
  };

  const csvData = [
    ["Identity", "Severity", "Info", "URL", "Header Match", "Body Match", "Status Code Match"],
    [
      results.identity || "",
      results.severity || "",
      results.info || "",
      results.url || "",
      results.header_match !== undefined ? (results.header_match ? "Yes" : "No") : "",
      results.body_match !== undefined ? (results.body_match ? "Yes" : "No") : "",
      results.status_code_match !== undefined ? (results.status_code_match ? "Yes" : "No") : "",
    ],
  ];

  

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Scan Details
      </Typography>
      <Box sx={{ mb: 2 }}>
        <CSVLink
          data={csvData}
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
      <Box sx={{ mt: 2, p: 2, borderRadius: 1, bgcolor: results.vulnerability ? "error.light" : "success.light" }}>
        <Typography variant="body1" fontWeight="bold">
          Identity: {results.identity || ""}
        </Typography>
        <Typography variant="body1" fontWeight="bold">
          Severity: {results.severity || ""}
        </Typography>
        <Typography variant="body1" fontWeight="bold">
          Info: {results.info || ""}
        </Typography>
        <Typography variant="body1" fontWeight="bold">
          URL: {results.url || ""}
        </Typography>
        {results.header_match !== undefined && (
          <Typography variant="body1" fontWeight="bold">
            Header Match: {results.header_match ? "Yes" : "No"}
          </Typography>
        )}
        {results.body_match !== undefined && (
          <Typography variant="body1" fontWeight="bold">
            Body Match: {results.body_match ? "Yes" : "No"}
          </Typography>
        )}
        {results.status_code_match !== undefined && (
          <Typography variant="body1" fontWeight="bold">
            Status Code Match: {results.status_code_match ? "Yes" : "No"}
          </Typography>
        )}
      </Box>
    </Box>
  );
  
}

export default ScanDetails;