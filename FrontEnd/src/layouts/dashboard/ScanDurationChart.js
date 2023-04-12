// in ScanDurationChart.js
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

function ScanDurationChart() {
  const [scanDurations, setScanDurations] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("/scan_durations");
        const data = await response.json();
        setScanDurations(data.scan_durations);
      } catch (error) {
        console.error("Error fetching scan durations:", error);
      }
    }
    fetchData();
  }, []);

  return (
    <LineChart width={500} height={300} data={scanDurations}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="scan_id" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="duration" stroke="#8884d8" />
    </LineChart>
  );
}

export default ScanDurationChart;
