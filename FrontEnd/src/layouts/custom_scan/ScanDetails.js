import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { CSVLink } from "react-csv";
import MDButton from "components/MDButton";
import jsPDF from "jspdf";
import "jspdf-autotable";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";


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
      ["Vulnerability", results.vulnerability !== undefined ? (results.vulnerability ? "Yes" : "No") : ""],
    ];
    

    doc.autoTable({
      theme: "grid",
      tableWidth: "wrap",
      body: tableRows,
    });

    doc.save("scan_results.pdf");
  };

  const csvData = [
    ["Identity", "Severity", "Info", "URL", "Header Match", "Body Match", "Status Code Match", "Vulnerability"],
    [
      results.identity || "",
      results.vulnerability !== undefined ? (results.vulnerability ? "Yes" : "No") : "",
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
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="scan details table">
          <TableHead>
            <TableRow sx={{ bgcolor: "primary.main" }}>
              <TableCell sx={{ color: "common.white", fontWeight: "bold" }}>Parameter</TableCell>
              <TableCell sx={{ color: "common.white", fontWeight: "bold" }}>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>Identity</TableCell>
              <TableCell>{results.identity || ""}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>Severity</TableCell>
              <TableCell>{results.severity || ""}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>Info</TableCell>
              <TableCell>{results.info || ""}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold" }}>URL</TableCell>
              <TableCell>{results.url || ""}</TableCell>
            </TableRow>
            {results.header_match !== undefined && (
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Header Match</TableCell>
                <TableCell>{results.header_match ? "Yes" : "No"}</TableCell>
              </TableRow>
            )}
            {results.body_match !== undefined && (
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Body Match</TableCell>
                <TableCell>{results.body_match ? "Yes" : "No"}</TableCell>
              </TableRow>
            )}
            {results.status_code_match !== undefined && (
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Status Code Match</TableCell>
                <TableCell>{results.status_code_match ? "Yes" : "No"}</TableCell>
              </TableRow>
            )}
            {results.vulnerability !== undefined && (
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Vulnerability</TableCell>
                <TableCell>{results.vulnerability ? "Yes" : "No"}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
  
  
  
              
  
  
  
  
}

export default ScanDetails;