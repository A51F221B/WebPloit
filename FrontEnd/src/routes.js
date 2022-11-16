/*
  For adding a new route you can follow the existing routes in the routes array.
  1. The `type` key with the `collapse` value is used for a route.
  2. The `type` key with the `title` value is used for a title inside the Sidenav. 
  3. The `type` key with the `divider` value is used for a divider between Sidenav items.
  4. The `name` key is used for the name of the route on the Sidenav.
  5. The `key` key is used for the key of the route (It will help you with the key prop inside a loop).
  6. The `icon` key is used for the icon of the route on the Sidenav, you have to add a node.
  7. The `collapse` key is used for making a collapsible item on the Sidenav that has other routes
  inside (nested routes), you need to pass the nested routes inside an array as a value for the `collapse` key.
  8. The `route` key is used to store the route location which is used for the react router.
  9. The `href` key is used to store the external links location.
  10. The `title` key is only for the item with the type of `title` and its used for the title text on the Sidenav.
  10. The `component` key is used to store the component of its route.
*/

// Material Dashboard 2 React layouts
import Dashboard from "layouts/dashboard";
import Tables from "layouts/tables";
import Vulnerability_Details from "layouts/vulnerability_details";
import Billing from "layouts/billing";
import RTL from "layouts/rtl";
import Notifications from "layouts/notifications";
import Profile from "layouts/profile";
import SignIn from "layouts/authentication/sign-in";
import SignUp from "layouts/authentication/sign-up";

// @mui icons
import Icon from "@mui/material/Icon";
import LogoutIcon from '@mui/icons-material/Logout';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import GitHubIcon from '@mui/icons-material/GitHub';
import ArticleIcon from '@mui/icons-material/Article';
import RadarIcon from '@mui/icons-material/Radar';
import DetailsIcon from '@mui/icons-material/Details';
import SpeedIcon from '@mui/icons-material/Speed';

import Quick_scan from "layouts/quick_scan";
import Custom_scan from "layouts/custom_scan";
// import Vulnerability_Details from "layouts/vulnerability_details";

const routes = [
  {
    type: "collapse",
    name: "Home",
    key: "dashboard",
    icon: <HomeIcon fontSize="small">dashboard</HomeIcon>,
    route: "/dashboard",
    component: <Dashboard />,
  },
  {
    type: "collapse",
    name: "Quick Scan",
    key: "quick-scan",
    icon: <SpeedIcon fontSize="small">quick-scan</SpeedIcon>,
    route: "/quick-scan",
    component: <Quick_scan />,
  },
  {
    type: "collapse",
    name: "Custom Scan",
    key: "custom-scan",
    icon: <RadarIcon fontSize="small">custom-scan</RadarIcon>,
    route: "/custom-scan",
    component: <Custom_scan />,
  },
  {
    type: "collapse",
    name: "Vulnerability Details",
    key: "vulnerability-details",
    icon: <DetailsIcon fontSize="small">vulnerability-details</DetailsIcon>,
    route: "/vulnerability-details",
    component: <Vulnerability_Details />,
  },
  // {
  //   type: "collapse",
  //   name: "Project Info",
  //   key: "project-info",
  //   icon: <InfoIcon fontSize="small">table_view</InfoIcon>,
  //   route: "/project-info",
  //   component: <Tables />,
  // },
  // {
  //   type: "collapse",
  //   name: "Billing",
  //   key: "billing",
  //   icon: <Icon fontSize="small">receipt_long</Icon>,
  //   route: "/billing",
  //   component: <Billing />,
  // },
  // {
  //   type: "collapse",
  //   name: "Documentation",
  //   key: "documentation",
  //   icon: <ArticleIcon fontSize="small">documentation</ArticleIcon>,
  //   route: "/project-documentation",
  //   component: <Tables />,
  // },
  // {
  //   type: "collapse",
  //   name: "Scan",
  //   key: "documentation",
  //   icon: <ArticleIcon fontSize="small">scan</ArticleIcon>,
  //   route: "/scan",
  //   component: <Tables />,
  // },
  // {
  //   type: "collapse",
  //   name: "RTL",
  //   key: "rtl",
  //   icon: <Icon fontSize="small">format_textdirection_r_to_l</Icon>,
  //   route: "/rtl",
  //   component: <RTL />,
  // },
  // {
  //   type: "collapse",
  //   name: "Notifications",
  //   key: "notifications",
  //   icon: <Icon fontSize="small">notifications</Icon>,
  //   route: "/notifications",
  //   component: <Notifications />,
  // },
  // {
  //   type: "collapse",
  //   name: "Profile",
  //   key: "profile",
  //   icon: <Icon fontSize="small">person</Icon>,
  //   route: "/profile",
  //   component: <Profile />,
  // },
  // {
  //   type: "collapse",
  //   name: "Sign In",
  //   key: "sign-in",
  //   icon: <Icon fontSize="small">login</Icon>,
  //   route: "/authentication/sign-in",
  //   component: <SignIn />,
  // },
  {
    type: "collapse",
    name: "Sign Out",
    key: "sign-up",
    icon: <LogoutIcon fontSize="small">sign-out</LogoutIcon>,
    route: "/authentication/sign-in",
    component: <SignIn />,
  },
];

export default routes;
