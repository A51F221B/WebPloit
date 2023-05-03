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
  if (!results || results.length === 0) {
    return null;
  }

  const exportPDF = () => {
    const doc = new jsPDF();
    let currentPageY = 30; // Start tracking the current Y position on the page
  
    // Add border around the page
    doc.setLineWidth(1);
    doc.rect(10, 10, 190, 277);
  
    // Add heading
    doc.setFontSize(20);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(30, 144, 255); // DodgerBlue
    doc.text("Webploit Scan Report", 14, 20);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0); // Reset text color to black
  
    // Add scan time
    const currentTime = new Date();
    const formattedTime = currentTime.toLocaleString();
    doc.setFontSize(14);
    doc.text(`Scan time: ${formattedTime}`, 14, currentPageY);
  
    results.forEach((result, index) => {
      doc.setFontSize(16);
      doc.setTextColor(255, 69, 0); // OrangeRed
      doc.text(`Scan Details: ${result.vuln}`, 14, currentPageY + 20);
      doc.setFontSize(12);
      doc.setTextColor(0, 0, 0); // Reset text color to black
  
      const tableRows = [
        ["Parameter", "Value"],
        ...Object.entries(result.data).map(([key, value]) => [
          key,
          typeof value === "boolean" ? (value ? "Yes" : "No") : value,
        ]),
      ];
  
      doc.autoTable({
        startY: currentPageY + 30,
        headStyles: { fillColor: "#1976d2", textColor: "#fff", fontStyle: "bold" },
        bodyStyles: { textColor: "#333" },
        margin: { top: 20 },
        tableWidth: 185,
        body: tableRows,
        alternateRowStyles: { fillColor: "#f0f0f0" }, // Add alternating row colors
      });
  
      // Update the current Y position after adding the table
      currentPageY = doc.previousAutoTable.finalY;
  
      // Check if there is enough space for the next Scan Details section
      if (currentPageY + 80 > 287) {
        doc.addPage();
        doc.rect(10, 10, 190, 277); // Add border to the new page
        currentPageY = 20; // Reset the Y position for the new page
      } else {
        currentPageY += 20; // Add space between sections
      }
    });
  
    doc.save("scan_results.pdf");
  };
  
  
  
  
  
  
  
  
  

  const csvData = [
    [
      "Vulnerability",
      "Identity",
      "Severity",
      "Info",
      "URL",
      "Header Match",
      "Body Match",
      "Status Code Match",
      "Vulnerability",
    ],
    ...results.map((result) => [
      result.vuln,
      result.data.identity || "",
      result.data.severity || "",
      result.data.info || "",
      result.data.url || "",
      result.data.header_match !== undefined
        ? result.data.header_match
          ? "Yes"
          : "No"
        : "",
      result.data.body_match !== undefined
        ? result.data.body_match
          ? "Yes"
          : "No"
        : "",
      result.data.status_code_match !== undefined
        ? result.data.status_code_match
          ? "Yes"
          : "No"
        : "",
      result.data.vulnerability !== undefined
        ? result.data.vulnerability
          ? "Yes"
          : "No"
        : "",
    ]),
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
      {results.map((result, index) => (
        <TableContainer component={Paper} key={index} sx={{ marginBottom: 2 }}>
          <Table sx={{ minWidth: 650 }} aria-label={`scan details table ${index}`}>
            <TableHead>
              <TableRow sx={{ bgcolor: "primary.main" }}>
                <TableCell sx={{ color: "common.white", fontWeight: "bold" }}>
                  Parameter
                </TableCell>
                <TableCell sx={{ color: "common.white", fontWeight: "bold" }}>
                  Value
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Vulnerability</TableCell>
                <TableCell>{result.vuln}</TableCell>
              </TableRow>
              {Object.entries(result.data).map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell sx={{ fontWeight: "bold" }}>{key}</TableCell>
                  <TableCell>
                    {typeof value === "boolean" ? (value ? "Yes" : "No") : value}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ))}
    </Box>
  );
  
}

export default ScanDetails;