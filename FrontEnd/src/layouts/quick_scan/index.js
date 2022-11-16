// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDButton from "components/MDButton";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import DataTable from "examples/Tables/DataTable";

import Button from 'react-bootstrap/Button';

// Data
import QuickScanData from "layouts/quick_scan/data/QuickScanData";
import MDBadge from "components/MDBadge";
// import projectsTableData from "layouts/tables/data/projectsTableData";
import React, { useState } from "react";

function Quick_scan() {
  const { columns, rows } = QuickScanData();
  // const { columns: pColumns, rows: pRows } = projectsTableData();


  

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
                  Quick Scan
                </MDTypography>
              </MDBox>
              <div style={{margin:"30px 20px"}}>
                <input style={{width:"50%", borderRadius:"12px 12px", padding:"10px", fontSize:"16px"}} placeholder="Enter URL to scan"></input>
                {/* <MDBox ml={-1} style={{margin:"20px -5px"}}>
                  <MDBadge badgeContent="Scan" color="info" variant="gradient" size="lg"/>
                </MDBox> */}
                <div style={{margin:"20px 0px"}}>
                  <MDButton variant="gradient" color="info" size="lg">Scan</MDButton>
                </div>
              </div>
              <MDBox pt={3}>
                {/* <DataTable
                  table={{ columns, rows }}
                  isSorted={false}
                  entriesPerPage={false}
                  showTotalEntries={false}
                  noEndBorder
                /> */}
              </MDBox>
            </Card>
          </Grid>
          {/* <Grid item xs={12}>
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
                  Progress Statistics
                </MDTypography>
              </MDBox>
              <MDBox pt={3}>
                <DataTable
                  table={{ columns: pColumns, rows: pRows }}
                  isSorted={false}
                  entriesPerPage={false}
                  showTotalEntries={false}
                  noEndBorder
                />
              </MDBox>
            </Card>
          </Grid> */}
        </Grid>
      </MDBox>
      {/* <Footer /> */}
    </DashboardLayout>
  );


}

export default Quick_scan;
