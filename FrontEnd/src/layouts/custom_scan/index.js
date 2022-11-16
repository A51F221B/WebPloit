// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import "styles.css"

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
import CustomScanData from "layouts/custom_scan/data/CustomScanData";
import MDBadge from "components/MDBadge";
// import projectsTableData from "layouts/tables/data/projectsTableData";

function Custom_scan() {
  const { columns, rows } = CustomScanData();
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
                  Custom Scan
                </MDTypography>
              </MDBox>
              <div style={{margin:"30px 20px"}}>
                <input style={{width:"50%", borderRadius:"12px 12px", padding:"10px", fontSize:"16px"}} placeholder="Enter URL to scan"></input>
                {/* <MDBox ml={-1} style={{margin:"20px -5px"}}>
                  <MDBadge badgeContent="Scan" color="info" variant="gradient" size="lg"/>
                </MDBox> */}
                <h5 style={{marginTop:"20px"}}>Select the vulnerabilities to scan</h5>
                <form>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="unionBasedSQLi" name="vul1" style={{}}/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>Union Based SQLi</label><br></br>
                  </div>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="blindSQLi" name="vul2"/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>Blind SQLi</label><br></br>
                  </div>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="reflectedxss" name="vul3"/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>Reflected XSS</label><br></br>
                  </div>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="storedxss" name="vul4"/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>Stored XSS</label><br></br>
                  </div>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="openRedirect" name="vul5"/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>Open Redirect</label><br></br>
                  </div>
                  <div className="selectBox">
                    <input className="selectButton" type="checkbox" id="xxe" name="vul6"/>
                    <label style={{fontSize:"16px", marginLeft:"10px"}}>XML External</label><br></br>
                  </div>
                </form>
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

export default Custom_scan;
