import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDButton from "components/MDButton";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import QuickScanData from "layouts/quick_scan/data/QuickScanData";
import { styled } from "@mui/material/styles";
import withAuth from "./withAuth";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

const EndpointList = styled("div")({
  display: "flex",
  flexDirection: "column",
  gap: "10px",
  alignItems: "flex-start",
  overflow: "auto",
  height: "400px",
  padding: "0px 10px",
  border: "1px solid rgba(224, 224, 224, 1)",
  borderRadius: "5px",
  margin: "10px 0px",
});

const EndpointItem = styled("div")({
  fontSize: "16px",
  fontWeight: "bold",
  color: "rgba(33, 150, 243, 1)",
  cursor: "pointer",
  transition: "all 0.2s",
  "&:hover": {
    color: "rgba(33, 150, 243, 0.7)",
  },
});

function EndpointParser() {
  const { columns, rows } = QuickScanData();
  const [url, setUrl] = useState("");
  const [scanResults, setScanResults] = useState(null);
  const [vulnerability, setVulnerability] = useState("openredirect");

  const handleScanClick = async () => {
    // Check if the URL is valid
    const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
    if (!urlRegex.test(url)) {
      alert("Invalid URL provided. Please enter a valid URL.");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:5000/api/endpoints", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          vulns: vulnerability,
        }),
        credentials: "include",
      });
  
      const data = await response.json();
  
      if (response.ok) {
        const endpoints = data.data.map((url) => ({ endpoint: url }));
        setScanResults(endpoints);
      } else {
        // Handle API errors
        console.error("Error scanning URL:", data);
        alert(`Error: ${data.message}`);
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
                  Endpoint Parser
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
                <FormControl
                  variant="standard"
                  style={{ marginLeft: "20px", marginBottom: "20px" }}
                >
                  <InputLabel id="vulnerability-label">Vulnerability</InputLabel>
                  <Select
                    labelId="vulnerability-label"
                    id="vulnerability-select"
                    value={vulnerability}
                    onChange={(e) => setVulnerability(e.target.value)}
                  >
                    <MenuItem value="openredirect">Open Redirect</MenuItem>
                    <MenuItem value="sqli">SQLi</MenuItem>
                    <MenuItem value="sqlipost">SQLi POST</MenuItem>
                    <MenuItem value="xxe">XXE</MenuItem>
                    <MenuItem value="xss">XSS</MenuItem>
                  </Select>
                </FormControl>
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
                    <table
                      style={{ borderCollapse: "collapse", width: "100%" }}
                    >
                      <thead>
                        <tr>
                          <th
                            style={{
                              backgroundColor: "#007aff",
                              color: "white",
                              padding: "10px 20px",
                              textAlign: "left",
                              borderBottom: "1px solid #ddd",
                            }}
                          >
                            Found Endpoints
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {scanResults.map((result, index) => (
                          <tr key={index}>
                            <td
                              style={{
                                padding: "10px 20px",
                                borderBottom:
                                  index === scanResults.length - 1
                                    ? "none"
                                    : "1px solid #ddd",
                              }}
                            >
                              {result.endpoint}
                            </td>
                          </tr>
                        ))}
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

export default withAuth(EndpointParser);
