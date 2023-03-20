import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import "styles.css";

import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDButton from "components/MDButton";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

import ScanDetails from "./ScanDetails"; // Import the new ScanDetails component

function Custom_scan() {
  const [url, setUrl] = useState("");
  const [vulnerabilities, setVulnerabilities] = useState({});
  const [message, setMessage] = useState("");
  const [results, setResults] = useState(null);

  const handleVulnerabilityChange = (event) => {
    setVulnerabilities({
      ...vulnerabilities,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const selectedVulns = Object.keys(vulnerabilities).filter(
      (key) => vulnerabilities[key]
    );

    try {
      const response = await fetch("http://localhost:5000/api/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, vuln: selectedVulns.join(",") }),
      });

      const data = await response.json();
      setMessage(data.message);

      if (data.status === "success") {
        setResults(data.data);
      } else {
        setResults(null);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessage("An error occurred. Please try again.");
      setResults(null);
    }
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <div style={{ margin: "30px 20px" }}>
                <form onSubmit={handleSubmit}>
                  <input
                    style={{
                      width: "50%",
                      borderRadius: "12px 12px",
                      padding: "10px",
                      fontSize: "16px",
                    }}
                    placeholder="Enter URL to scan"
                    value={url}
                    onChange={(event) => setUrl(event.target.value)}
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={vulnerabilities.xxe || false}
                        onChange={handleVulnerabilityChange}
                        name="xxe"
                        color="primary"
                      />
                    }
                    label="XML External Entity (XXE)"
                  />
                  {/* ... */}
                  {/* (your other checkboxes) */}
                  {/* ... */}
                  <div style={{ margin: "20px 0px" }}>
                    <MDButton type="submit" variant="gradient" color="info" size="lg">
                      Scan
                    </MDButton>
                  </div>
                </form>
                {message && (
                  <div style={{ marginTop: "10px" }}>
                    <MDTypography color={results ? "success" : "error"}>
                      {message}
                    </MDTypography>
                  </div>
                )}
                <ScanDetails results={results} />
              </div>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
    </DashboardLayout>
 

  );
  
  
}

export default Custom_scan;
