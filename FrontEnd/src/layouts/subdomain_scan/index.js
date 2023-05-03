import React, { useState } from "react";
import { useTable } from "react-table";
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
import ErrorBoundary from "./ErrorBoundary";


const headerCellStyle = {
  padding: "12px 24px",
  borderBottom: "1px solid #e0e0e0",
  backgroundColor: "#2196f3",
  fontWeight: "bold",
  color: "white",
};


function SubdomainScan() {
  const { columns, rows } = QuickScanData();
  const [url, setUrl] = useState("");
  const [scanResults, setScanResults] = useState(null);

  const handleScanClick = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/subdomains", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          aggressive: true,
        }),
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        const formattedData = data.data.map((item) => ({
          ip_address: item.subdomain,
          subdomain: item.ip_address,
          server: item.server,
          code: item.code,
        }));
        setScanResults(formattedData);
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
                  Subdomain Scan
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
                    <ErrorBoundary>
                      <table style={{ borderCollapse: "collapse", width: "100%" }}>
                        <thead>
                          <tr>
                            <th style={headerCellStyle}>IP Address</th>
                            <th style={headerCellStyle}>Subdomain</th>
                            <th style={headerCellStyle}>Server</th>
                            <th style={headerCellStyle}>Code</th>
                          </tr>
                        </thead>
                        <tbody>
                          {scanResults.map((result) => (
                            <tr key={result.ip_address}>
                              <td style={{ padding: "12px 24px", borderBottom: "1px solid #e0e0e0" }}>
                                {result.ip_address}
                              </td>
                              <td style={{ padding: "12px 24px", borderBottom: "1px solid #e0e0e0" }}>
                                {result.subdomain}
                              </td>
                              <td style={{ padding: "12px 24px", borderBottom: "1px solid #e0e0e0" }}>
                                {result.server}
                              </td>
                              <td style={{ padding: "12px 24px", borderBottom: "1px solid #e0e0e0" }}>
                                {result.code}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </ErrorBoundary>
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

export default withAuth(SubdomainScan);