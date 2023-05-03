import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDButton from "components/MDButton";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import withAuth from "./withAuth";

function DeepScan() {
  const [url, setUrl] = useState("");
  const [vuln, setVuln] = useState("openredirect");
  const [scanResults, setScanResults] = useState(null);

  const handleVulnChange = (event) => {
    setVuln(event.target.value);
  };

  const headerCellStyle = {
    padding: "12px 24px",
    borderBottom: "1px solid #e0e0e0",
    backgroundColor: "#2196f3",
    fontWeight: "bold",
    color: "white",
  };
  


  const handleScanClick = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/deepscan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          vuln: vuln,
        }),
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        setScanResults(data.results);
      } else {
        console.error("Failed to scan URL");
      }
    } catch (error) {
      console.error("Error scanning URL:", error);
    }
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <MDBox
                mx={2}
                mt={-3}
                py={3}
                px={2}
                variant="gradient"
                bgColor="info"
                borderRadius="lg"
                coloredShadow="info"
              >
                <MDTypography variant="h6" color="white">
                  Deep Scan
                </MDTypography>
              </MDBox>
              <div style={{ margin: "30px 20px" }}>
                <input
                  style={{
                    width: "50%",
                    borderRadius: "12px 12px",
                    padding: "10px",
                    fontSize: "16px",
                  }}
                  placeholder="Enter URL to scan"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                ></input>
                <Select
                  value={vuln}
                  onChange={handleVulnChange}
                  style={{ marginLeft: "10px" }}
                >
                  <MenuItem value="openredirect">Open Redirect</MenuItem>
                  <MenuItem value="sqli">SQL Injection</MenuItem>
                  <MenuItem value="sqlipost">SQL Injection POST</MenuItem>
                  <MenuItem value="xxe">XXE</MenuItem>
                  <MenuItem value="xss">XSS</MenuItem>
                </Select>
                <div style={{ margin: "20px 0px" }}>
                  <MDButton
                    variant="gradient"
                    color="info"
                    size="lg"
                    onClick={handleScanClick}
                  >
                    Scan
                  </MDButton>
                </div>
              </div>
              <MDBox pt={3}>
  {scanResults && (
    <div style={{ overflowX: "auto" }}>
      <table style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th style={headerCellStyle}>Vulnerability</th>
            <th style={headerCellStyle}>Identity</th>
            <th style={headerCellStyle}>URL</th>
            {scanResults.some((result) => result.data.status_code_match !== undefined) && (
              <th style={headerCellStyle}>Status Code Match</th>
            )}
            {scanResults.some((result) => result.data.header_match !== undefined) && (
              <th style={headerCellStyle}>Header Match</th>
            )}
            {scanResults.some((result) => result.data.body_match !== undefined) && (
              <th style={headerCellStyle}>Body Match</th>
            )}
            <th style={headerCellStyle}>Vulnerable</th>
          </tr>
        </thead>
        <tbody>
          {scanResults.map((result, index) => {
            const rowCellStyle = {
              padding: "10px 20px",
              borderBottom:
                index === scanResults.length - 1 ? "none" : "1px solid #ddd",
            };

            return (
              <tr key={index}>
                <td style={rowCellStyle}>{result.vuln}</td>
                <td style={rowCellStyle}>{result.data.identity}</td>
                <td style={rowCellStyle}>{result.data.url}</td>
                {result.data.status_code_match !== undefined && (
                  <td style={rowCellStyle}>
                    {result.data.status_code_match ? "Yes" : "No"}
                  </td>
                )}
                {result.data.header_match !== undefined && (
                  <td style={rowCellStyle}>
                    {result.data.header_match ? "Yes" : "No"}
                  </td>
                )}
                {result.data.body_match !== undefined && (
                  <td style={rowCellStyle}>
                    {result.data.body_match ? "Yes" : "No"}
                  </td>
                )}
                <td style={rowCellStyle}>
                  {result.data.vulnerability ? "Yes" : "No"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  )}
</MDBox>
                              </Card>
                              </Grid>
                              </Grid>
                              </MDBox>
                              </DashboardLayout>
 );  

}

export default withAuth(DeepScan);