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

function SubdomainScanTable({ columns, data }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <table {...getTableProps()} style={{ border: 'solid 1px black', width: '100%' }}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th
                {...column.getHeaderProps()}
                style={{
                  borderBottom: 'solid 3px black',
                  background: 'aliceblue',
                  color: 'black',
                  fontWeight: 'bold',
                }}
              >
                {column.render('Header')}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => {
                return (
                  <td
                    {...cell.getCellProps()}
                    style={{
                      padding: '10px',
                      border: 'solid 1px gray',
                      background: 'papayawhip',
                    }}
                  >
                    {cell.render('Cell')}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

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
                      <SubdomainScanTable
                        columns={[
                          { Header: "IP Address", accessor: "ip_address" },
                          { Header: "Subdomain", accessor: "subdomain" },
                          { Header: "Server", accessor: "server" },
                          { Header: "Code", accessor: "code" },
                        ]}
                        data={scanResults}
                      />
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
